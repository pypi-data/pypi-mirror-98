from firebase_admin.messaging import AndroidFCMOptions


class AndroidFCMOptionsConfigBuilder:
    def __init__(self):
        self._android_fcm_options = AndroidFCMOptions()

    def build(self):
        return self._android_fcm_options


class AndroidFCMOptionsAnalyticsLabelBuilder(AndroidFCMOptionsConfigBuilder):

    def analytics_label(self, analytics_label=None):
        self._android_fcm_options.analytics_label = analytics_label
        return self


class AndroidFCMOptionsBuilder(AndroidFCMOptionsAnalyticsLabelBuilder):

    @classmethod
    def config(cls):
        return AndroidFCMOptionsBuilder()



