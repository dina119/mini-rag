from fastapi import FastAPI,APIRouter,Depends,UploadFile
import os
from Helpers.config import getSettings
from Controllers import DataController

data_Router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_Router.post("/upload/{project_id}")
async def uploaFile(project_id:str,file:UploadFile,AppSetting=Depends(getSettings)):
    IsValid=DataController().Validate_Uploaded_File(file=file)
    return IsValid