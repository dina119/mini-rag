from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
import os
from Helpers.config import getSettings
from Controllers import DataController
from fastapi.responses import  JSONResponse

data_Router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_Router.post("/upload/{project_id}")
async def uploaFile(project_id:str,file:UploadFile,AppSetting=Depends(getSettings)):
    IsValid,resultSignal=DataController().Validate_Uploaded_File(file=file)
    if  not IsValid :
         return JSONResponse(
             status_code=status.HTTP_400_BAD_REQUEST,
             content={
                 "Signal":resultSignal
             }
         )
        
    
        
    
   