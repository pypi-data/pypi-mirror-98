from firebase_admin.messaging import APNSPayload


class APNSPayloadConfigBuilder:
    def __init__(self):
        self._apns_payload_config = APNSPayload()

    def build(self):
        return self._apns_payload_config


class APNSPayloadAPSBuilder(APNSPayloadConfigBuilder):
    # aps: A ``messaging.Aps`` instance to be included in the payload.
    def aps(self, aps):
        self._apns_payload_config.aps = aps
        return self


class APNSPayloadCustomDataBuilder(APNSPayloadAPSBuilder):
    # kwargs: Arbitrary keyword arguments to be included as custom fields in the payload
    def custom_data(self, **kwargs):
        self._apns_payload_config.custom_data = kwargs
        return self


class APNSPayloadBuilder(APNSPayloadCustomDataBuilder):

    @classmethod
    def config(cls):
        return APNSPayloadBuilder()
