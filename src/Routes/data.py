from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
import os
from Helpers.config import getSettings
from Controllers import DataController,ProjectController
from fastapi.responses import  JSONResponse
import aiofiles
from Models import Response_Signal
import logging

logger=logging.getLogger('uvicorn.error')

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
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_Path=DataController().generate_filename(original_filename=file.filename,project_id=project_id)
       
    try:
            async with aiofiles.open(file_Path,"+wb")as f:
                while chunk:= await file.read(AppSetting.FILE_DEFAULT_CHUNKSIZE):
                    await file.write(chunk)
    except Exception as e:
        logger.error(f"error in uploading file",e)
        return JSONResponse(
             status_code=status.HTTP_400_BAD_REQUEST,
             content={
                 "Signal":Response_Signal.FILE_UPLOAD_FAILED
             }
         )
        
    
    return JSONResponse(
             
             content={
                 "Signal":Response_Signal.FILE_UPLOAD_SUCCESS.value
             }
         )
        
    
        
    
   