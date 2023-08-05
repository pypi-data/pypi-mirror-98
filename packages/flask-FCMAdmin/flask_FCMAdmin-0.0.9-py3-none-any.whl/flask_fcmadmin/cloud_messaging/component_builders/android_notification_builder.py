from firebase_admin.messaging import AndroidNotification
from flask_fcmadmin.cloud_messaging.utils.priority_type import Priority
from flask_fcmadmin.cloud_messaging.utils.visibility_type import Visibility


class AndroidNotificationConfigBuilder:

    def __init__(self):
        self._android_notification_config = AndroidNotification()

    def build(self):
        return self._android_notification_config


class AndroidNotificationTitleBuilder(AndroidNotificationConfigBuilder):
    # title: Title of the notification (optional). If specified, overrides the title set via
    #             ``messaging.Notification``.
    def android_notification_title(self, title):
        self._android_notification_config.title = title
        return self


class AndroidNotificationBodyBuilder(AndroidNotificationTitleBuilder):
    # body: Body of the notification (optional). If specified, overrides the body set via
    #             ``messaging.Notification``.
    def android_notification_body(self, body):
        self._android_notification_config.body = body
        return self


class AndroidNotificationIconBuilder(AndroidNotificationBodyBuilder):
    # icon: Icon of the notification (optional)
    def android_notification_icon(self, icon):
        self._android_notification_config.icon = icon
        return self


class AndroidNotificationColorBuilder(AndroidNotificationIconBuilder):
    # color: Color of the notification icon expressed in ``#rrggbb`` form (optional).
    def android_notification_color(self, color):
        self._android_notification_config.color = color
        return self


class AndroidNotificationSoundBuilder(AndroidNotificationColorBuilder):
    # sound: Sound to be played when the device receives the notification (optional). This is
    #             usually the file name of the sound resource.
    def android_notification_sound(self, sound):
        self._android_notification_config.sound = sound
        return self


class AndroidNotificationTagBuilder(AndroidNotificationSoundBuilder):
    # tag: Tag of the notification (optional). This is an identifier used to replace existing
    #             notifications in the notification drawer. If not specified, each request creates a new
    #             notification.
    def android_notification_tag(self, tag):
        self._android_notification_config.tag = tag
        return self


class AndroidNotificationClickActionBuilder(AndroidNotificationTagBuilder):
    # click_action: The action associated with a user click on the notification (optional). If
    #             specified, an activity with a matching intent filter is launched when a user clicks on
    #             the notification.
    def android_notification_click_action(self, click_action):
        self._android_notification_config.click_action = click_action
        return self


class AndroidNotificationBodyLocKeyBuilder(AndroidNotificationClickActionBuilder):
    # body_loc_key: Key of the body string in the app's string resources to use to localize the
    #             body text (optional).
    def android_notification_body_loc_key(self, body_loc_key):
        self._android_notification_config.body_loc_key = body_loc_key
        return self


class AndroidNotificationBodyLocArgsBuilder(AndroidNotificationBodyLocKeyBuilder):
    # body_loc_args: A list of resource keys that will be used in place of the format specifiers
    #             in ``body_loc_key`` (optional).
    def android_notification_body_loc_args(self, body_loc_args):
        self._android_notification_config.body_loc_args = body_loc_args
        return self


class AndroidNotificationTitleLocKeyBuilder(AndroidNotificationBodyLocArgsBuilder):
    # title_loc_key: Key of the title string in the app's string resources to use to localize the
    #             title text (optional).
    def android_notification_title_loc_key(self, title_loc_key):
        self._android_notification_config.title_loc_key = title_loc_key
        return self


class AndroidNotificationTitleLocArgsBuilder(AndroidNotificationTitleLocKeyBuilder):
    # title_loc_args: A list of resource keys that will be used in place of the format specifiers
    #             in ``title_loc_key`` (optional).
    def android_notification_title_loc_args(self, title_loc_args):
        self._android_notification_config.title_loc_args = title_loc_args
        return self


class AndroidNotificationChannelIDBuilder(AndroidNotificationTitleLocArgsBuilder):
    # channel_id: channel_id of the notification (optional).
    def android_notification_channel_id(self, channel_id):
        self._android_notification_config.channel_id = channel_id
        return self


class AndroidNotificationImageBuilder(AndroidNotificationChannelIDBuilder):
    # image: Image url of the notification (optional).
    def android_notification_image(self, image):
        self._android_notification_config.image = image
        return self


class AndroidNotificationTickerBuilder(AndroidNotificationImageBuilder):
    # ticker: Sets the ``ticker`` text, which is sent to accessibility services. Prior to API
    #             level 21 (Lollipop), sets the text that is displayed in the status bar when the
    #             notification first arrives (optional).
    def android_notification_ticker(self, ticker):
        self._android_notification_config.ticker = ticker
        return self


class AndroidNotificationStickyBuilder(AndroidNotificationTickerBuilder):
    # sticky: When set to ``False`` or unset, the notification is automatically dismissed when the
    #             user clicks it in the panel. When set to ``True``, the notification persists even when
    #             the user clicks it (optional).
    def android_notification_sticky(self, sticky):
        self._android_notification_config.sticky = sticky
        return self


class AndroidNotificationEventTimestampBuilder(AndroidNotificationStickyBuilder):
    # event_timestamp: For notifications that inform users about events with an absolute time
    #             reference, sets the time that the event in the notification occurred as a
    #             ``datetime.datetime`` instance. If the ``datetime.datetime`` instance is naive, it
    #             defaults to be in the UTC timezone. Notifications in the panel are sorted by this time
    #             (optional).
    def android_notification_event_timestamp(self, event_timestamp):
        self._android_notification_config.event_timestamp = event_timestamp
        return self


class AndroidNotificationLocalOnlyBuilder(AndroidNotificationEventTimestampBuilder):
    # local_only: Sets whether or not this notification is relevant only to the current device.
    #             Some notifications can be bridged to other devices for remote display, such as a Wear OS
    #             watch. This hint can be set to recommend this notification not be bridged (optional).
    #             See Wear OS guides:
    #             https://developer.android.com/training/wearables/notifications/bridger#existing-method-of-preventing-bridging
    def android_notification_local_only(self, local_only):
        self._android_notification_config.local_only = local_only
        return self



class AndroidNotificationPriorityBuilder(AndroidNotificationLocalOnlyBuilder):
    # priority: Sets the relative priority for this notification. Low-priority notifications may
    #             be hidden from the user in certain situations. Note this priority differs from
    #             ``AndroidMessagePriority``. This priority is processed by the client after the message
    #             has been delivered. Whereas ``AndroidMessagePriority`` is an FCM concept that controls
    #             when the message is delivered (optional). Must be one of ``default``, ``min``, ``low``,
    #             ``high``, ``max`` or ``normal``.
    def android_notification_default_priority(self):
        self._android_notification_config.priority = Priority.DEFAULT.value
        return self

    def android_notification_min_priority(self):
        self._android_notification_config.priority = Priority.MIN.value
        return self

    def android_notification_low_priority(self):
        self._android_notification_config.priority = Priority.LOW.value
        return self

    def android_notification_high_priority(self):
        self._android_notification_config.priority = Priority.HIGH.value
        return self

    def android_notification_max_priority(self):
        self._android_notification_config.priority = Priority.MAX.value
        return self

    def android_notification_normal_priority(self):
        self._android_notification_config.priority = Priority.NORMAL.value
        return self


class AndroidNotificationVibrateTimingsMillisBuilder(AndroidNotificationPriorityBuilder):
    # vibrate_timings_millis: Sets the vibration pattern to use. Pass in an array of milliseconds
    #             to turn the vibrator on or off. The first value indicates the duration to wait before
    #             turning the vibrator on. The next value indicates the duration to keep the vibrator on.
    #             Subsequent values alternate between duration to turn the vibrator off and to turn the
    #             vibrator on. If ``vibrate_timings`` is set and ``default_vibrate_timings`` is set to
    #             ``True``, the default value is used instead of the user-specified ``vibrate_timings``.
    def android_notification_vibrate_timings_millis(self, vibrate_timings_millis):
        self._android_notification_config.vibrate_timings_millis = vibrate_timings_millis
        return self


class AndroidNotificationDefaultVibrateTimingsBuilder(AndroidNotificationPriorityBuilder):
    # default_vibrate_timings: If set to ``True``, use the Android framework's default vibrate
    #             pattern for the notification (optional). Default values are specified in ``config.xml``
    #             https://android.googlesource.com/platform/frameworks/base/+/master/core/res/res/values/config.xml.
    #             If ``default_vibrate_timings`` is set to ``True`` and ``vibrate_timings`` is also set,
    #             the default value is used instead of the user-specified ``vibrate_timings``.
    def android_notification_default_vibrate_timings(self, default_vibrate_timings):
        self._android_notification_config.default_vibrate_timings = default_vibrate_timings
        return self


class AndroidNotificationDefaultSoundBuilder(AndroidNotificationDefaultVibrateTimingsBuilder):
    # default_sound: If set to ``True``, use the Android framework's default sound for the
    #             notification (optional). Default values are specified in ``config.xml``
    #             https://android.googlesource.com/platform/frameworks/base/+/master/core/res/res/values/config.xml
    def android_notification_default_sound(self, default_sound):
        self._android_notification_config.default_sound = default_sound
        return self


class AndroidNotificationLightSettingsBuilder(AndroidNotificationDefaultSoundBuilder):
    # light_settings: Settings to control the notification's LED blinking rate and color if LED is
    #             available on the device. The total blinking time is controlled by the OS (optional).
    def android_notification_light_settings(self, light_settings):
        self._android_notification_config.light_settings = light_settings
        return self


class AndroidNotificationDefaultLightSettingsBuilder(AndroidNotificationLightSettingsBuilder):
    # default_light_settings: If set to ``True``, use the Android framework's default LED light
    #             settings for the notification. Default values are specified in ``config.xml``
    #             https://android.googlesource.com/platform/frameworks/base/+/master/core/res/res/values/config.xml.
    #             If ``default_light_settings`` is set to ``True`` and ``light_settings`` is also set, the
    #             user-specified ``light_settings`` is used instead of the default value.
    def android_notification_default_light_settings(self, default_light_settings):
        self._android_notification_config.default_light_settings = default_light_settings
        return self


class AndroidNotificationVisibilityBuilder(AndroidNotificationDefaultLightSettingsBuilder):
    # visibility: Sets the visibility of the notification. Must be either ``private``, ``public``,
    #             or ``secret``. If unspecified, default to ``private``.
    def android_notification_private_visibility(self):
        self._android_notification_config.visibility = Visibility.PRIVATE.value
        return self

    def android_notification_public_visibility(self):
        self._android_notification_config.visibility = Visibility.PUBLIC.value
        return self

    def android_notification_secret_visibility(self):
        self._android_notification_config.visibility = Visibility.SECRET.value
        return self


class AndroidNotificationNotificationCountBuilder(AndroidNotificationVisibilityBuilder):
    # notification_count: Sets the number of items this notification represents. May be displayed
    #             as a badge count for Launchers that support badging. See ``NotificationBadge``
    #             https://developer.android.com/training/notify-user/badges. For example, this might be
    #             useful if you're using just one notification to represent multiple new messages but you
    #             want the count here to represent the number of total new messages. If zero or
    #             unspecified, systems that support badging use the default, which is to increment a
    #             number displayed on the long-press menu each time a new notification arrives.
    def android_notification_notification_count(self, notification_count):
        self._android_notification_config.notification_count = notification_count
        return self


class AndroidNotificationBuilder(AndroidNotificationNotificationCountBuilder):

    @classmethod
    def config(cls):
        return AndroidNotificationBuilder()

