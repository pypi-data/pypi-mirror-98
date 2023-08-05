from firebase_admin.messaging import Notification


class NotificationConfigBuilder:
    def __init__(self):
        self._notification_config = Notification()

    def build(self):
        return self._notification_config


class NotificationTitleBuilder(NotificationConfigBuilder):
    # title: Title of the notification (optional)
    def title(self, title):
        self._notification_config.title = title
        return self


class NotificationBodyBuilder(NotificationTitleBuilder):
    # body: Body of the notification (optional)
    def body(self, body):
        self._notification_config.body = body
        return self


class NotificationImageBuilder(NotificationBodyBuilder):
    # image: Image url of the notification (optional)
    def image(self, image):
        self._notification_config.image = image
        return self


class NotificationBuilder(NotificationImageBuilder):

    @classmethod
    def config(cls):
        return NotificationBuilder()

