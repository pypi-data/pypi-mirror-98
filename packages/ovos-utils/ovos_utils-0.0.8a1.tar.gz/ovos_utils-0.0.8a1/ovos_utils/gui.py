from ovos_utils.system import is_installed, has_screen
from ovos_utils import resolve_ovos_resource_file, resolve_resource_file
from ovos_utils.messagebus import wait_for_reply, get_mycroft_bus, Message
from ovos_utils.log import LOG
from collections import namedtuple
import time
from os.path import join
from enum import IntEnum


def can_display():
    return has_screen()


def is_gui_installed():
    return is_installed("mycroft-gui-app")


def is_gui_connected(bus=None):
    # bus api for https://github.com/MycroftAI/mycroft-core/pull/2682
    # send "gui.status.request"
    # receive "gui.status.request.response"
    response = wait_for_reply("gui.status.request",
                              "gui.status.request.response", bus=bus)
    if response:
        return response.data["connected"]
    return False


class GUIPlaybackStatus(IntEnum):
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    UNDEFINED = 3


class GUITracker:
    """ Replicates GUI API from mycroft-core,
    does not interact with GUI but exactly mimics status"""
    Namespace = namedtuple('Namespace', ['name', 'pages'])
    RESERVED_KEYS = ['__from', '__idle']
    IDLE_MESSAGE = "mycroft.mark2.collect_idle"  # TODO this will change

    def __init__(self, bus=None,
                 host='0.0.0.0', port=8181, route='/core', ssl=False):
        self.bus = bus or get_mycroft_bus(host, port, route, ssl)
        self._active_skill = None
        self._is_idle = False
        self.idle_ts = 0
        # This datastore holds the data associated with the GUI provider. Data
        # is stored in Namespaces, so you can have:
        # self.datastore["namespace"]["name"] = value
        # Typically the namespace is a meaningless identifier, but there is a
        # special "SYSTEM" namespace.
        self._datastore = {}

        # self.loaded is a list, each element consists of a namespace named
        # tuple.
        # The namespace namedtuple has the properties "name" and "pages"
        # The name contains the namespace name as a string and pages is a
        # mutable list of loaded pages.
        #
        # [Namespace name, [List of loaded qml pages]]
        # [
        # ["SKILL_NAME", ["page1.qml, "page2.qml", ... , "pageN.qml"]
        # [...]
        # ]
        self._loaded = []  # list of lists in order.

        # Listen for new GUI clients to announce themselves on the main bus
        self._active_namespaces = []

        # GUI handlers
        self.bus.on("gui.value.set", self._on_gui_set_value)
        self.bus.on("gui.page.show", self._on_gui_show_page)
        self.bus.on("gui.page.delete", self._on_gui_delete_page)
        self.bus.on("gui.clear.namespace", self._on_gui_delete_namespace)

        # Idle screen handlers TODO message cleanup...
        self._idle_screens = {}
        self.bus.on("mycroft.device.show.idle", self._on_show_idle)  # legacy
        self.bus.on(self.IDLE_MESSAGE, self._on_show_idle)
        self.bus.on("mycroft.mark2.register_idle", self._on_register_idle)

        self.bus.emit(Message("mycroft.mark2.collect_idle"))

    @staticmethod
    def is_gui_installed():
        return is_gui_installed()

    def is_gui_connected(self):
        return is_gui_connected(self.bus)

    @staticmethod
    def can_display():
        return can_display()

    def is_displaying(self):
        return self.active_skill is not None

    def is_idle(self):
        return self._is_idle

    @property
    def active_skill(self):
        return self._active_skill

    @property
    def gui_values(self):
        return self._datastore

    @property
    def idle_screens(self):
        return self._idle_screens

    @property
    def active_namespaces(self):
        return self._active_namespaces

    @property
    def gui_pages(self):
        return self._loaded

    # GUI event handlers
    # user can/should subclass this
    def on_idle(self, namespace):
        pass

    def on_active(self, namespace):
        pass

    def on_new_page(self, namespace, page, index):
        pass

    def on_delete_page(self, namespace, index):
        pass

    def on_gui_value(self, namespace, key, value):
        pass

    def on_new_namespace(self, namespace):
        pass

    def on_move_namespace(self, namespace, from_index, to_index):
        pass

    def on_remove_namespace(self, namespace, index):
        pass

    ######################################################################
    # GUI client API
    # TODO see how much of this can be removed
    @staticmethod
    def _get_page_data(message):
        """ Extract page related data from a message.

        Args:
            message: messagebus message object
        Returns:
            tuple (page, namespace, index)
        Raises:
            ValueError if value is missing.
        """
        data = message.data
        # Note:  'page' can be either a string or a list of strings
        if 'page' not in data:
            raise ValueError("Page missing in data")
        if 'index' in data:
            index = data['index']
        else:
            index = 0
        page = data.get("page", "")
        namespace = data.get("__from", "")
        return page, namespace, index

    def _set(self, namespace, name, value):
        """ Perform the send of the values to the connected GUIs. """
        if namespace not in self._datastore:
            self._datastore[namespace] = {}
        if self._datastore[namespace].get(name) != value:
            self._datastore[namespace][name] = value

    def __find_namespace(self, namespace):
        for i, skill in enumerate(self._loaded):
            if skill[0] == namespace:
                return i
        return None

    def __insert_pages(self, namespace, pages):
        """ Insert pages into the namespace

        Args:
            namespace (str): Namespace to add to
            pages (list):    Pages (str) to insert
        """
        LOG.debug("Inserting new pages")
        # Insert the pages into local reprensentation as well.
        updated = self.Namespace(self._loaded[0].name,
                                 self._loaded[0].pages + pages)
        self._loaded[0] = updated

    def __remove_page(self, namespace, pos):
        """ Delete page.

        Args:
            namespace (str): Namespace to remove from
            pos (int):      Page position to remove
        """
        LOG.debug("Deleting {} from {}".format(pos, namespace))
        self.on_delete_page(namespace, pos)
        # Remove the page from the local reprensentation as well.
        self._loaded[0].pages.pop(pos)

    def __insert_new_namespace(self, namespace, pages):
        """ Insert new namespace and pages.

        This first sends a message adding a new namespace at the
        highest priority (position 0 in the namespace stack)

        Args:
            namespace (str):  The skill namespace to create
            pages (str):      Pages to insert (name matches QML)
        """
        LOG.debug("Inserting new namespace")
        self.on_new_namespace(namespace)
        # Make sure the local copy is updated
        self._loaded.insert(0, self.Namespace(namespace, pages))
        if time.time() - self.idle_ts > 1:
            # we cant know if this page is idle or not, but when it is we
            # received a idle event within the same second
            self._is_idle = False
            self.on_active(namespace)
        else:
            self.on_idle(namespace)

    def __move_namespace(self, from_pos, to_pos):
        """ Move an existing namespace to a new position in the stack.

        Args:
            from_pos (int): Position in the stack to move from
            to_pos (int): Position to move to
        """
        LOG.debug("Activating existing namespace")
        # Move the local representation of the skill from current
        # position to position 0.
        namespace = self._loaded[from_pos].name
        self.on_move_namespace(namespace, from_pos, to_pos)
        self._loaded.insert(to_pos, self._loaded.pop(from_pos))

    def _show(self, namespace, page, index):
        """ Show a page and load it as needed.

        Args:
            page (str or list): page(s) to show
            namespace (str):  skill namespace
            index (int): ??? TODO: Unused in code ???

        TODO: - Update sync to match.
              - Separate into multiple functions/methods
        """

        LOG.debug("GUIConnection activating: " + namespace)
        self._active_skill = namespace
        pages = page if isinstance(page, list) else [page]

        # find namespace among loaded namespaces
        try:
            index = self.__find_namespace(namespace)
            if index is None:
                # This namespace doesn't exist, insert them first so they're
                # shown.
                self.__insert_new_namespace(namespace, pages)
                return
            else:  # Namespace exists
                if index > 0:
                    # Namespace is inactive, activate it by moving it to
                    # position 0
                    self.__move_namespace(index, 0)

                # Find if any new pages needs to be inserted
                new_pages = [p for p in pages if
                             p not in self._loaded[0].pages]
                if new_pages:
                    self.__insert_pages(namespace, new_pages)
        except Exception as e:
            LOG.exception(repr(e))

    ######################################################################
    # Internal GUI events
    def _on_gui_set_value(self, message):
        data = message.data
        namespace = data.get("__from", "")

        # Pass these values on to the GUI renderers
        for key in data:
            if key not in self.RESERVED_KEYS:
                try:
                    self._set(namespace, key, data[key])
                    self.on_gui_value(namespace, key, data[key])
                except Exception as e:
                    LOG.exception(repr(e))

    def _on_gui_delete_page(self, message):
        """ Bus handler for removing pages. """
        page, namespace, _ = self._get_page_data(message)
        try:
            self._remove_pages(namespace, page)
        except Exception as e:
            LOG.exception(repr(e))

    def _on_gui_delete_namespace(self, message):
        """ Bus handler for removing namespace. """
        try:
            namespace = message.data['__from']
            self._remove_namespace(namespace)
        except Exception as e:
            LOG.exception(repr(e))

    def _on_gui_show_page(self, message):
        try:
            page, namespace, index = self._get_page_data(message)
            # Pass the request to the GUI(s) to pull up a page template
            self._show(namespace, page, index)
            self.on_new_page(namespace, page, index)
        except Exception as e:
            LOG.exception(repr(e))

    def _remove_namespace(self, namespace):
        """ Remove namespace.

        Args:
            namespace (str): namespace to remove
        """
        index = self.__find_namespace(namespace)
        if index is None:
            return
        else:
            LOG.debug("Removing namespace {} at {}".format(namespace, index))
            self.on_remove_namespace(namespace, index)
            # Remove namespace from loaded namespaces
            self._loaded.pop(index)

    def _remove_pages(self, namespace, pages):
        """ Remove the listed pages from the provided namespace.

        Args:
            namespace (str):    The namespace to modify
            pages (list):       List of page names (str) to delete
        """
        try:
            index = self.__find_namespace(namespace)
            if index is None:
                return
            else:
                # Remove any pages that doesn't exist in the namespace
                pages = [p for p in pages if p in self._loaded[index].pages]
                # Make sure to remove pages from the back
                indexes = [self._loaded[index].pages.index(p) for p in pages]
                indexes = sorted(indexes)
                indexes.reverse()
                for page_index in indexes:
                    self.__remove_page(namespace, page_index)
        except Exception as e:
            LOG.exception(repr(e))

    def _on_register_idle(self, message):
        """Handler for catching incoming idle screens."""
        if "name" in message.data and "id" in message.data:
            screen = message.data["name"]
            if screen not in self._idle_screens:
                self.bus.on("{}.idle".format(message.data["id"]),
                            self._on_show_idle)
            self._idle_screens[screen] = message.data["id"]
            LOG.info("Registered {}".format(message.data["name"]))
        else:
            LOG.error("Malformed idle screen registration received")

    def _on_show_idle(self, message):
        self.idle_ts = time.time()
        self._is_idle = True


class GUIInterface:
    """Interface to the Graphical User Interface, allows interaction with
    the mycroft-gui from anywhere

    Values set in this class are synced to the GUI, accessible within QML
    via the built-in sessionData mechanism.  For example, in Python you can
    write in a skill:
        self.gui['temp'] = 33
        self.gui.show_page('Weather.qml')
    Then in the Weather.qml you'd access the temp via code such as:
        text: sessionData.time
    """

    def __init__(self, skill_id, bus=None, remote_server=None):
        self.bus = bus or get_mycroft_bus()
        self.__session_data = {}  # synced to GUI for use by this skill's pages
        self.page = None  # the active GUI page (e.g. QML template) to show
        self.skill_id = skill_id
        self.on_gui_changed_callback = None
        self.remote_url = remote_server
        self._events = []
        self.video_info = None
        self.setup_default_handlers()

    @property
    def connected(self):
        """Returns True if at least 1 gui is connected, else False"""
        return is_gui_connected(self.bus)

    # events
    def setup_default_handlers(self):
        """Sets the handlers for the default messages."""
        self.register_handler('set', self.handle_gui_set)
        # should be emitted by self.play_video
        self.register_handler('playback.ended',
                              self.handle_gui_stop)

    def register_handler(self, event, handler):
        """Register a handler for GUI events.

        will be prepended with self.skill_id.XXX if missing in event

        When using the triggerEvent method from Qt
        triggerEvent("event", {"data": "cool"})

        Arguments:
            event (str):    event to catch
            handler:        function to handle the event
        """
        if not event.startswith(f'{self.skill_id}.'):
            event = f'{self.skill_id}.' + event
        self._events.append((event, handler))
        self.bus.on(event, handler)

    def set_on_gui_changed(self, callback):
        """Registers a callback function to run when a value is
        changed from the GUI.

        Arguments:
            callback:   Function to call when a value is changed
        """
        self.on_gui_changed_callback = callback

    def send_event(self, event_name, params=None):
        """Trigger a gui event.

        Arguments:
            event_name (str): name of event to be triggered
            params: json serializable object containing any parameters that
                    should be sent along with the request.
        """
        params = params or {}
        self.bus.emit(Message("gui.event.send",
                              {"__from": self.skill_id,
                               "event_name": event_name,
                               "params": params}))

    # internals
    def handle_gui_stop(self, message):
        """Stop video playback in gui"""
        self.stop_video()

    def handle_gui_set(self, message):
        """Handler catching variable changes from the GUI.

        Arguments:
            message: Messagebus message
        """
        for key in message.data:
            self[key] = message.data[key]
        if self.on_gui_changed_callback:
            self.on_gui_changed_callback()

    def __setitem__(self, key, value):
        """Implements set part of dict-like behaviour with named keys."""
        self.__session_data[key] = value

        if self.page:
            # emit notification (but not needed if page has not been shown yet)
            data = self.__session_data.copy()
            data.update({'__from': self.skill_id})
            self.bus.emit(Message("gui.value.set", data))

    def __getitem__(self, key):
        """Implements get part of dict-like behaviour with named keys."""
        return self.__session_data[key]

    def get(self, *args, **kwargs):
        """Implements the get method for accessing dict keys."""
        return self.__session_data.get(*args, **kwargs)

    def __contains__(self, key):
        """Implements the "in" operation."""
        return self.__session_data.__contains__(key)

    def _pages2uri(self, page_names):
        # Convert pages to full reference
        page_urls = []
        for name in page_names:
            page = resolve_resource_file(name) or \
                   resolve_resource_file(join('ui', name)) or \
                   resolve_ovos_resource_file(name) or \
                   resolve_ovos_resource_file(join('ui', name))

            if page:
                if self.remote_url:
                    page_urls.append(self.remote_url + "/" + page)
                elif page.startswith("file://"):
                    page_urls.append(page)
                else:
                    page_urls.append("file://" + page)
            else:
                LOG.error("Unable to find page: {}".format(name))
        return page_urls

    def shutdown(self):
        """Shutdown gui interface.

        Clear pages loaded through this interface and remove the bus events
        """
        self.release()
        self.video_info = None
        for event, handler in self._events:
            self.bus.remove(event, handler)

    # base gui interactions
    def show_page(self, name, override_idle=None,
                  override_animations=False):
        """Begin showing the page in the GUI

        Arguments:
            name (str): Name of page (e.g "mypage.qml") to display
            override_idle (boolean, int):
                True: Takes over the resting page indefinitely
                (int): Delays resting page for the specified number of
                       seconds.
            override_animations (boolean):
                True: Disables showing all platform skill animations.
                False: 'Default' always show animations.
        """
        self.show_pages([name], 0, override_idle, override_animations)

    def show_pages(self, page_names, index=0, override_idle=None,
                   override_animations=False):
        """Begin showing the list of pages in the GUI.

        Arguments:
            page_names (list): List of page names (str) to display, such as
                               ["Weather.qml", "Forecast.qml", "Details.qml"]
            index (int): Page number (0-based) to show initially.  For the
                         above list a value of 1 would start on "Forecast.qml"
            override_idle (boolean, int):
                True: Takes over the resting page indefinitely
                (int): Delays resting page for the specified number of
                       seconds.
            override_animations (boolean):
                True: Disables showing all platform skill animations.
                False: 'Default' always show animations.
        """
        if not isinstance(page_names, list):
            raise ValueError('page_names must be a list')

        if index > len(page_names):
            raise ValueError('Default index is larger than page list length')

        self.page = page_names[index]

        # First sync any data...
        data = self.__session_data.copy()
        data.update({'__from': self.skill_id})
        self.bus.emit(Message("gui.value.set", data))
        page_urls = self._pages2uri(page_names)
        self.bus.emit(Message("gui.page.show",
                              {"page": page_urls,
                               "index": index,
                               "__from": self.skill_id,
                               "__idle": override_idle,
                               "__animations": override_animations}))

    def remove_page(self, page):
        """Remove a single page from the GUI.

        Arguments:
            page (str): Page to remove from the GUI
        """
        return self.remove_pages([page])

    def remove_pages(self, page_names):
        """Remove a list of pages in the GUI.

        Arguments:
            page_names (list): List of page names (str) to display, such as
                               ["Weather.qml", "Forecast.qml", "Other.qml"]
        """
        if not isinstance(page_names, list):
            page_names = [page_names]
        page_urls = self._pages2uri(page_names)
        self.bus.emit(Message("gui.page.delete",
                              {"page": page_urls,
                               "__from": self.skill_id}))

    def clear(self):
        """Reset the value dictionary, and remove namespace from GUI.

        This method does not close the GUI for a Skill. For this purpose see
        the `release` method.
        """
        self.__session_data = {}
        self.page = None
        self.bus.emit(Message("gui.clear.namespace",
                              {"__from": self.skill_id}))

    def release(self):
        """Signal that this skill is no longer using the GUI,
        allow different platforms to properly handle this event.
        Also calls self.clear() to reset the state variables
        Platforms can close the window or go back to previous page"""
        self.clear()
        self.bus.emit(Message("mycroft.gui.screen.close",
                              {"skill_id": self.skill_id}))

    # Utils / Templates
    def show_text(self, text, title=None, override_idle=None,
                  override_animations=False):
        """Display a GUI page for viewing simple text.

        Arguments:
            text (str): Main text content.  It will auto-paginate
            title (str): A title to display above the text content.
            override_idle (boolean, int):
                True: Takes over the resting page indefinitely
                (int): Delays resting page for the specified number of
                       seconds.
            override_animations (boolean):
                True: Disables showing all platform skill animations.
                False: 'Default' always show animations.
        """
        self["text"] = text
        self["title"] = title
        self.show_page("SYSTEM_TextFrame.qml", override_idle,
                       override_animations)

    def show_image(self, url, caption=None,
                   title=None, fill=None,
                   override_idle=None, override_animations=False):
        """Display a GUI page for viewing an image.

        Arguments:
            url (str): Pointer to the image
            caption (str): A caption to show under the image
            title (str): A title to display above the image content
            fill (str): Fill type supports 'PreserveAspectFit',
            'PreserveAspectCrop', 'Stretch'
            override_idle (boolean, int):
                True: Takes over the resting page indefinitely
                (int): Delays resting page for the specified number of
                       seconds.
            override_animations (boolean):
                True: Disables showing all platform skill animations.
                False: 'Default' always show animations.
        """
        self["image"] = url
        self["title"] = title
        self["caption"] = caption
        self["fill"] = fill
        self.show_page("SYSTEM_ImageFrame.qml", override_idle,
                       override_animations)

    def show_animated_image(self, url, caption=None,
                            title=None, fill=None,
                            override_idle=None, override_animations=False):
        """Display a GUI page for viewing an image.

        Arguments:
            url (str): Pointer to the .gif image
            caption (str): A caption to show under the image
            title (str): A title to display above the image content
            fill (str): Fill type supports 'PreserveAspectFit',
            'PreserveAspectCrop', 'Stretch'
            override_idle (boolean, int):
                True: Takes over the resting page indefinitely
                (int): Delays resting page for the specified number of
                       seconds.
            override_animations (boolean):
                True: Disables showing all platform skill animations.
                False: 'Default' always show animations.
        """
        self["image"] = url
        self["title"] = title
        self["caption"] = caption
        self["fill"] = fill
        self.show_page("SYSTEM_AnimatedImageFrame.qml", override_idle,
                       override_animations)

    def show_html(self, html, resource_url=None, override_idle=None,
                  override_animations=False):
        """Display an HTML page in the GUI.

        Arguments:
            html (str): HTML text to display
            resource_url (str): Pointer to HTML resources
            override_idle (boolean, int):
                True: Takes over the resting page indefinitely
                (int): Delays resting page for the specified number of
                       seconds.
            override_animations (boolean):
                True: Disables showing all platform skill animations.
                False: 'Default' always show animations.
        """
        self["html"] = html
        self["resourceLocation"] = resource_url
        self.show_page("SYSTEM_HtmlFrame.qml", override_idle,
                       override_animations)

    def show_url(self, url, override_idle=None,
                 override_animations=False):
        """Display an HTML page in the GUI.

        Arguments:
            url (str): URL to render
            override_idle (boolean, int):
                True: Takes over the resting page indefinitely
                (int): Delays resting page for the specified number of
                       seconds.
            override_animations (boolean):
                True: Disables showing all platform skill animations.
                False: 'Default' always show animations.
        """
        self["url"] = url
        self.show_page("SYSTEM_UrlFrame.qml", override_idle,
                       override_animations)

    def show_confirmation_status(self, text="", override_idle=False,
                                 override_animations=False):
        # NOT YET PRed to mycroft-core, taken from gez-mycroft wifi GUI test skill
        self.clear()
        self["icon"] = resolve_ovos_resource_file("ui/icons/check-circle.svg")
        self["label"] = text
        self["bgColor"] = "#40DBB0"
        self.show_page("SYSTEM_status.qml", override_idle=override_idle,
                       override_animations=override_animations)

    def show_error_status(self, text="", override_idle=False,
                          override_animations=False):
        # NOT YET PRed to mycroft-core, taken from gez-mycroft wifi GUI test skill
        self.clear()
        self["icon"] = resolve_ovos_resource_file("ui/icons/times-circle.svg")
        self["label"] = text
        self["bgColor"] = "#FF0000"
        self.show_page("SYSTEM_status.qml", override_idle=override_idle,
                       override_animations=override_animations)

    # Media playback interactions
    def play_video(self, url, title="", repeat=None, override_idle=True,
                   override_animations=True):
        """ Play video stream

        Arguments:
            url (str): URL of video source
            title (str): Title of media to be displayed
            repeat (boolean, int):
                True: Infinitly loops the current video track
                (int): Loops the video track for specified number of
                times.
            override_idle (boolean, int):
                True: Takes over the resting page indefinitely
                (int): Delays resting page for the specified number of
                       seconds.
            override_animations (boolean):
                True: Disables showing all platform skill animations.
                False: 'Default' always show animations.
        """
        self["playStatus"] = "play"
        self["video"] = url
        self["title"] = title
        self["playerRepeat"] = repeat
        self.video_info = {"title": title, "url": url}
        self.show_page("SYSTEM_VideoPlayer.qml",
                       override_idle=override_idle,
                       override_animations=override_animations)

    @property
    def is_video_displayed(self):
        """Returns whether the gui is in a video playback state.
        Eg if the video is paused, it would still be displayed on screen
        but the video itself is not "playing" so to speak"""
        return self.video_info is not None

    @property
    def playback_status(self):
        """Returns gui playback status,
        indicates if gui is playing, paused or stopped"""
        if self.__session_data.get("playStatus", -1) == "play":
            return GUIPlaybackStatus.PLAYING
        if self.__session_data.get("playStatus", -1) == "pause":
            return GUIPlaybackStatus.PAUSED
        if self.__session_data.get("playStatus", -1) == "stop":
            return GUIPlaybackStatus.STOPPED
        return GUIPlaybackStatus.UNDEFINED

    def pause_video(self):
        """Pause video playback."""
        if self.is_video_displayed:
            self["playStatus"] = "pause"

    def stop_video(self):
        """Stop video playback."""
        if self.is_video_displayed:
            self["playStatus"] = "stop"
            self.release()
        self.video_info = None

    def resume_video(self):
        """Resume paused video playback."""
        if self.__session_data.get("playStatus", "stop") == "pause":
            self["playStatus"] = "play"


if __name__ == "__main__":
    from ovos_utils import wait_for_exit_signal

    LOG.set_level("DEBUG")
    g = GUITracker()
    wait_for_exit_signal()
