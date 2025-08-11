from Helpers.config import getSettings
import os
import random
import string
class BaseController:
    def __init__(self):
        self.app_settings=getSettings()
        self.base_dir=os.path.dirname(os.path.dirname(__file__))
        self.file_dir=os.path.join(
            self.base_dir,
            "assets/files"
        )
        
    def generate_random_string(self,length=8):
      characters = string.ascii_letters + string.digits
      return ''.join(random.choice(characters) for _ in range(length))

