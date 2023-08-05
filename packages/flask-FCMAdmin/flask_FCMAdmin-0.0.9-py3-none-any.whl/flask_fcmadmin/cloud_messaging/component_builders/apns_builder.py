from firebase_admin.messaging import APNSConfig


class APNSConfigBuilder:
    def __init__(self):
        self._apns_config = APNSConfig()

    def build(self):
        return self._apns_config


class APNSHeadersConfig(APNSConfigBuilder):
    # headers: A dictionary of headers (optional).
    def headers(self, headers):
        self._apns_config.headers = headers
        return self


class APNSPayloadConfig(APNSHeadersConfig):
    # payload: A ``messaging.APNSPayload`` to be included in the message (optional).
    def payload(self, payload):
        self._apns_config.payload = payload
        return self


class APNSFCMOptionsConfig(APNSPayloadConfig):
    # fcm_options: A ``messaging.APNSFCMOptions`` instance to be included in the message
    #       (optional).
    def fcm_options(self, fcm_options):
        self._apns_config.fcm_options = fcm_options
        return self


class APNSBuilder(APNSFCMOptionsConfig):

    @classmethod
    def config(cls):
        return APNSBuilder()
