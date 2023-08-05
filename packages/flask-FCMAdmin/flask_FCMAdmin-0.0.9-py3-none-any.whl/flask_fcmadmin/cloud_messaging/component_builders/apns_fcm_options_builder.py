from firebase_admin.messaging import APNSFCMOptions


class APNSFCMOptionsConfigBuilder:
    def __init__(self):
        self._apns_fcm_options = APNSFCMOptions()

    def build(self):
        return self._apns_fcm_options


class APNSFCMOptionsAnalyticsLabelBuilder(APNSFCMOptionsConfigBuilder):

    def analytics_label(self, analytics_label=None):
        self._apns_fcm_options.analytics_label = analytics_label
        return self


class APNSFCMOptionsBuilder(APNSFCMOptionsAnalyticsLabelBuilder):

    @classmethod
    def config(cls):
        return APNSFCMOptionsBuilder()
