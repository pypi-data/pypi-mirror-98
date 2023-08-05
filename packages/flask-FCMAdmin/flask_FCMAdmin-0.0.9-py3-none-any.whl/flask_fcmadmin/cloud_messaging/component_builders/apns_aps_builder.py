from firebase_admin.messaging import Aps

# Aps dictionary to be included in an APNS payload
class APNSApsConfigBuilder:
    def __init__(self):
        self._aps_config = Aps()

    def build(self):
        return self._aps_config


class APNSApsAlertConfig(APNSApsConfigBuilder):
    # alert: A string or a ``messaging.ApsAlert`` instance (optional).
    def alert(self, alert):
        self._aps_config.alert = alert
        return self


class APNSApsBadgeConfig(APNSApsAlertConfig):
    # badge: A number representing the badge to be displayed with the message (optional).
    def badge(self, badge):
        self._aps_config.badge = badge
        return self


class APNSApsSoundConfig(APNSApsBadgeConfig):
    # sound: Name of the sound file to be played with the message or a
    #             ``messaging.CriticalSound`` instance (optional).
    def sound(self, sound):
        self._aps_config.sound = sound
        return self


class APNSApsContentAvailableConfig(APNSApsSoundConfig):
    # content_available: A boolean indicating whether to configure a background update
    #             notification (optional).
    def content_available(self, content_available):
        self._aps_config.content_available = content_available
        return self


class APNSApsCategoryConfig(APNSApsContentAvailableConfig):
    # category: String identifier representing the message type (optional).
    def category(self, category):
        self._aps_config.category = category
        return self


class APNSApsThreadIDConfig(APNSApsCategoryConfig):
    # thread_id: An app-specific string identifier for grouping messages (optional).
    def thread_id(self, thread_id):
        self._aps_config.thread_id = thread_id
        return self


class APNSApsMutableContentConfig(APNSApsThreadIDConfig):
    #  mutable_content: A boolean indicating whether to support mutating notifications at
    #             the client using app extensions (optional).
    def mutable_content(self, mutable_content):
        self._aps_config.mutable_content = mutable_content
        return self


class APNSApsCustomDataConfig(APNSApsMutableContentConfig):
    # custom_data: A dict of custom key-value pairs to be included in the Aps dictionary
    #             (optional).
    def custom_data(self, custom_data):
        self._aps_config.custom_data = custom_data
        return self


class APNSApsBuilder(APNSApsCustomDataConfig):

    @classmethod
    def config(cls):
        return APNSApsBuilder()
