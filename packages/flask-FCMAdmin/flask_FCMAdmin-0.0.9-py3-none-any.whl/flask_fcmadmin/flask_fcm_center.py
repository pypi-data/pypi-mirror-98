from firebase_admin import credentials
import firebase_admin


class FlaskFCMCenter:

    def __init__(self, prefix="FCM_ADMIN", instance_name="DEFAULT"):
        self._firebase_admin = None
        self.prefix = prefix
        self.instance_name = instance_name
        self._file = None

    def init_app(self, app, file):
        # Get flask app config file content
        # config = app.config
        cred = credentials.Certificate(file)
        self._file = file
        self._firebase_admin = firebase_admin.initialize_app(credential=cred, name=self.instance_name.lower())

        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions[f"{self.prefix}_{self.instance_name}".lower()] = self

    def __getattr__(self, name):
        return getattr(self._firebase_admin, name)

    def __getitem__(self, name):
        return self._firebase_admin[name]

    @property
    def app(self):
        return self._firebase_admin
