from fastapi import FastAPI,APIRouter,Depends,UploadFile
from .BaseController import BaseController
from Models import Response_Signal
from .ProjectController import ProjectController
import re
import os
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
    
    def generate_filename(self,original_filename:str,project_id:str):
        random_filename=self.generate_random_string()
        file_path=ProjectController().get_project_path(project_id=project_id)
        cleaned_filename=self.get_cleaned_filename(original_filename=original_filename)
        new_filePath=os.path.join(
            file_path,
            random_filename+"_"+cleaned_filename
        )
        while os.path.exists(new_filePath):
            random_filename=self.generate_random_string()
            new_filePath=os.path.join(
            file_path,
            random_filename+"_"+cleaned_filename
        )
        return new_filePath
            
    
    def get_cleaned_filename(self,original_filename:str):
        cleaned_filename=re.sub(r'[^\w]','',original_filename.strip())
        cleaned_filename=cleaned_filename.replace(" ","_")
        return cleaned_filename
        