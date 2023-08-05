from firebase_admin.messaging import FCMOptions


class FCMOptionsConfigBuilder:
    def __init__(self):
        self._fcm_options = FCMOptions()

    def build(self):
        return self._fcm_options


class FCMOptionsAnalyticsLabelBuilder(FCMOptionsConfigBuilder):

    def analytics_label(self, analytics_label=None):
        self._fcm_options.analytics_label = analytics_label
        return self


class FCMOptionsBuilder(FCMOptionsAnalyticsLabelBuilder):

    @classmethod
    def config(cls):
        return FCMOptionsBuilder()