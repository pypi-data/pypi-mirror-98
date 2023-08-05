from firebase_admin.messaging import send, send_all, send_multicast
from firebase_admin.messaging import Message, MulticastMessage


class MessageBuilder:
    def __init__(self, dry_run=False, app=None):
        self._dry_run = dry_run
        self._app = app
        self._message = Message()

    def data(self, data):
        # data: A dictionary of data fields (optional). All keys and values in the dictionary must be
        #             strings.
        self._message.data = data
        return self

    def notification(self, notification):
        # notification: An instance of ``messaging.Notification`` (optional).
        self._message.notification = notification
        return self

    def android(self, android):
        # android: An instance of ``messaging.AndroidConfig`` (optional).
        self._message.android = android
        return self

    def webpush(self, webpush):
        # webpush: An instance of ``messaging.WebpushConfig`` (optional).
        self._message.webpush = webpush
        return self

    def apns(self, apns):
        # apns: An instance of ``messaging.ApnsConfig`` (optional).
        self._message.apns = apns
        return self

    def fcm_options(self, fcm_options):
        # fcm_options: An instance of ``messaging.FCMOptions`` (optional).
        self._message.fcm_options = fcm_options
        return self

    def token(self, token):
        # token: The registration token of the device to which the message should be sent (optional).
        self._message.token = token
        return self

    def topic(self, topic):
        # topic: Name of the FCM topic to which the message should be sent (optional). Topic name
        #             may contain the ``/topics/`` prefix.
        self._message.topic = topic
        return self

    def condition(self, condition):
        # condition: The FCM condition to which the message should be sent (optional).
        self._message.condition = condition
        return self

    def build_send(self):
        return send(message=self._message,
                    dry_run=self._dry_run,
                    app=self._app)


class MulticastMessageBuilder:
    def __init__(self, dry_run=False, app=None):
        self.FCM_MAX_RECIPIENTS = 500
        self._tokens = []
        self._dry_run = dry_run
        self._app = app
        self._multicast_message = MulticastMessage([])

    def append_token(self, token):
        self._tokens.append(token)
        return self

    def replace_tokens(self, tokens):
        self._tokens = tokens
        return self

    def data(self, data):
        # data: A dictionary of data fields (optional). All keys and values in the dictionary must be
        #             strings.
        self._multicast_message.data = data
        return self

    def notification(self, notification):
        # notification: An instance of ``messaging.Notification`` (optional).
        self._multicast_message.notification = notification
        return self

    def android(self, android):
        # android: An instance of ``messaging.AndroidConfig`` (optional).
        self._multicast_message.android = android
        return self

    def webpush(self, webpush):
        # webpush: An instance of ``messaging.WebpushConfig`` (optional).
        self._multicast_message.webpush = webpush
        return self

    def apns(self, apns):
        # apns: An instance of ``messaging.ApnsConfig`` (optional).
        self._multicast_message.apns = apns
        return self

    def fcm_options(self, fcm_options):
        # fcm_options: An instance of ``messaging.FCMOptions`` (optional).
        self._multicast_message.fcm_options = fcm_options
        return self

    def multicast_chunks_generator(self):
        for i in range(0, len(self._tokens), self.FCM_MAX_RECIPIENTS):
            self._multicast_message.tokens = self._tokens[i:i + self.FCM_MAX_RECIPIENTS]
            batch_response = send_multicast(multicast_message=self._multicast_message,
                                            dry_run=self._dry_run,
                                            app=self._app)

            yield BatchResponse(self._multicast_message.tokens, batch_response)


class BatchResponse:

    def __init__(self, tokens, batch_response):
        self._tokens = tokens
        self._batch_response = batch_response

    @property
    def failed_tokens(self):
        if self._batch_response.failure_count > 0:
            responses = self._batch_response.responses
            failed_tokens = []
            for index, resp in enumerate(responses):
                if not resp.success:
                    failed_tokens.append(self._tokens[index])
            return failed_tokens
        else:
            return []

    @property
    def failed_count(self):
        return self._batch_response.failure_count


# request error
# - exceptions.DeadlineExceededError
# - exceptions.UnavailableError
# - exceptions.UnknownError
# response error
# -