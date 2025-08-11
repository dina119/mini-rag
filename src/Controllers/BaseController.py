from Helpers.config import getSettings
import os
class BaseController:
    def __init__(self):
        self.app_settings=getSettings()
        self.base_dir=os.path.dirname(os.path.dirname(__file__))
        self.file_dir=os.path.join(
            self.base_dir,
            "assets/files"
        )

