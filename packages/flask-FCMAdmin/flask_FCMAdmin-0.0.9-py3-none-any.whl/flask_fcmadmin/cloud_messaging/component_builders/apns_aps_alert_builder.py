from firebase_admin.messaging import ApsAlert


# An alert that can be included in ``messaging.Aps``.
class APNSApsApsAlertConfigBuilder:
    def __init__(self):
        self._aps_alert = ApsAlert()

    def build(self):
        return self._aps_alert


class APNSApsAlertTitleBuilder(APNSApsApsAlertConfigBuilder):
    # title: Title of the alert (optional). If specified, overrides the title set via
    #             ``messaging.Notification``.
    def title(self, title):
        self._aps_alert.title = title
        return self


class APNSApsAlertSubtitleBuilder(APNSApsAlertTitleBuilder):
    # subtitle: Subtitle of the alert (optional).
    def subtitle(self, subtitle):
        self._aps_alert.critical = subtitle
        return self


class APNSApsAlertBodyBuilder(APNSApsAlertSubtitleBuilder):
    # body: Body of the alert (optional). If specified, overrides the body set via
    #             ``messaging.Notification``.
    def body(self, body):
        self._aps_alert.body = body
        return self


class APNSApsAlertLocKeyBuilder(APNSApsAlertBodyBuilder):
    # loc_key: Key of the body string in the app's string resources to use to localize the
    #             body text (optional).
    def loc_key(self, loc_key):
        self._aps_alert.loc_key = loc_key
        return self


class APNSApsAlertLocArgsBuilder(APNSApsAlertLocKeyBuilder):
    # loc_args: A list of resource keys that will be used in place of the format specifiers
    #             in ``loc_key`` (optional).
    def loc_args(self, loc_args):
        self._aps_alert.loc_args = loc_args
        return self


class APNSApsAlertTitleLocKeyBuilder(APNSApsAlertLocArgsBuilder):
    # title_loc_key: Key of the title string in the app's string resources to use to localize the
    #             title text (optional).
    def title_loc_key(self, title_loc_key):
        self._aps_alert.title_loc_key = title_loc_key
        return self


class APNSApsAlertTitleLocArgsBuilder(APNSApsAlertTitleLocKeyBuilder):
    # title_loc_args: A list of resource keys that will be used in place of the format specifiers
    #             in ``title_loc_key`` (optional).
    def title_loc_args(self, title_loc_args):
        self._aps_alert.title_loc_args = title_loc_args
        return self


class APNSApsAlertActionLocKeyBuilder(APNSApsAlertTitleLocArgsBuilder):
    # action_loc_key: Key of the text in the app's string resources to use to localize the
    #             action button text (optional).
    def action_loc_key(self, action_loc_key):
        self._aps_alert.action_loc_key = action_loc_key
        return self


class APNSApsAlertLaunchImageBuilder(APNSApsAlertActionLocKeyBuilder):
    # launch_image: Image for the notification action (optional).
    def launch_image(self, launch_image):
        self._aps_alert.launch_image = launch_image
        return self


class APNSApsAlertCustomDataBuilder(APNSApsAlertLaunchImageBuilder):
    # custom_data: A dict of custom key-value pairs to be included in the ApsAlert dictionary
    #             (optional)
    def custom_data(self, custom_data):
        self._aps_alert.custom_data = custom_data
        return self


class APNSApsApsAlertBuilder(APNSApsAlertCustomDataBuilder):

    @classmethod
    def config(cls):
        return APNSApsApsAlertBuilder()
