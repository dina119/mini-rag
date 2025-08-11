from Helpers.config import getSettings

class BaseController:
    def __init__(self):
        self.app_settings=getSettings()

