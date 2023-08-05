from firebase_admin.messaging import AndroidConfig


class AndroidConfigBuilder:
    def __init__(self):
        self._android_config = AndroidConfig()

    def build(self):
        return self._android_config


class AndroidCollapseKeyBuilder(AndroidConfigBuilder):
    # collapse_key: Collapse key string for the message (optional). This is an identifier for a
    #             group of messages that can be collapsed, so that only the last message is sent when
    #             delivery can be resumed. A maximum of 4 different collapse keys may be active at a
    #             given time.
    def collapse_key(self, collapse_key):
        self._android_config.collapse_key = collapse_key
        return self


class AndroidPriorityBuilder(AndroidCollapseKeyBuilder):
    # priority: Priority of the message (optional). Must be one of ``high`` or ``normal``.
    def priority(self, priority):
        self._android_config.priority = priority
        return self


class AndroidTTLBuilder(AndroidPriorityBuilder):
    # ttl: The time-to-live duration of the message (optional). This can be specified
    #             as a numeric seconds value or a ``datetime.timedelta`` instance.
    def ttl(self, duration):
        self._android_config.ttl = duration
        return self


class AndroidRestrictedPackageNameBuilder(AndroidTTLBuilder):
    # restricted_package_name: The package name of the application where the registration tokens
    #             must match in order to receive the message (optional).
    def restricted_package_name(self, restricted_package_name):
        self._android_config.restricted_package_name = restricted_package_name
        return self


class AndroidDataBuilder(AndroidRestrictedPackageNameBuilder):
    # data: A dictionary of data fields (optional). All keys and values in the dictionary must be
    #             strings. When specified, overrides any data fields set via ``Message.data``.
    def data(self, data):
        self._android_config.data = data
        return self


class AndroidNotificationBuilder(AndroidDataBuilder):
    # notification: A ``messaging.AndroidNotification`` to be included in the message (optional).
    def notification(self, notification):
        self._android_config.notification = notification
        return self


class AndroidFCMOptionsBuilder(AndroidNotificationBuilder):
    # fcm_options: A ``messaging.AndroidFCMOptions`` to be included in the message (optional).
    def fcm_options(self, fcm_options):
        self._android_config.fcm_options = fcm_options
        return self


class AndroidBuilder(AndroidFCMOptionsBuilder):

    @classmethod
    def config(cls):
        return AndroidBuilder()


