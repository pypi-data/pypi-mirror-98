from firebase_admin.messaging import CriticalSound


class APNSApsCriticalSoundConfigBuilder:
    def __init__(self):
        self.aps_critical_sound = CriticalSound()

    def build(self):
        return self.aps_critical_sound


class APNSApsNameBuilder(APNSApsCriticalSoundConfigBuilder):
    # name: The name of a sound file in your app's main bundle or in the ``Library/Sounds``
    #             folder of your app's container directory. Specify the string ``default`` to play the
    #             system sound.
    def name(self, name):
        self.aps_critical_sound.name = name
        return self


class APNSApsCriticalBuilder(APNSApsNameBuilder):
    # critical: Set to ``True`` to set the critical alert flag on the sound configuration
    #             (optional).
    def critical(self, critical=None):
        self.aps_critical_sound.critical = critical
        return self


class APNSApsVolumeBuilder(APNSApsCriticalBuilder):
    # volume: The volume for the critical alert's sound. Must be a value between 0.0 (silent)
    #             and 1.0 (full volume) (optional).
    def volume(self, volume=None):
        self.aps_critical_sound.volume = volume
        return self


class APNSApsCriticalSoundBuilder(APNSApsVolumeBuilder):

    @classmethod
    def config(cls):
        return APNSApsCriticalSoundBuilder()
