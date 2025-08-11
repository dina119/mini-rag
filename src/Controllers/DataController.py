from fastapi import FastAPI,APIRouter,Depends,UploadFile
from .BaseController import BaseController
from Models import Response_Signal

class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1048576
    
    def Validate_Uploaded_File(self,file:UploadFile):
        if file.content_type  not in self.app_settings.FILE_ALLOWED_TYPES:
           return False,Response_Signal.FILE_TYPE_NOTSUPPORTED.value
        if file.size>self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False , Response_Signal.FILE_MAX_SIZE_EXCEEDED.value
        return True , Response_Signal.FILE_VALIDATE_SUCCESS.value