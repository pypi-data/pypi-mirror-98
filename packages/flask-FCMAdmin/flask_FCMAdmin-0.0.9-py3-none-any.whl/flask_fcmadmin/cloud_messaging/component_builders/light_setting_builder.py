from firebase_admin.messaging import LightSettings


class LightSettingsConfigBuilder:
    def __init__(self, color, light_on_millis, light_off_mills):
        self._light_settings_config = LightSettings(color, light_on_millis, light_off_mills)

    def build(self):
        return self._light_settings_config


class LightSettingsBuilder(LightSettingsConfigBuilder):

    # color: Sets the color of the LED in ``#rrggbb`` or ``#rrggbbaa`` format.
    # light_on_duration_millis: Along with ``light_off_duration``, defines the blink rate of LED
    #             flashes.
    # light_on_duration_millis: Along with ``light_off_duration``, defines the blink rate of LED
    #             flashes.
    @classmethod
    def config_light_settings(cls, color, light_on_millis, light_off_mills):
        return LightSettingsBuilder(color, light_on_millis, light_off_mills)

