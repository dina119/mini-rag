from fastapi import FastAPI,APIRouter,Depends,UploadFile,status,Request
import os
from Helpers.config import getSettings
from Controllers import DataController,ProjectController,ProcessController
from fastapi.responses import  JSONResponse
import aiofiles
from Models import Response_Signal
import logging
from .Schemes.data import Process_Request
from Models import ProjectModel,ChunkModel
from Models.db_schemes.dataChunk import DataChunk
from qdrant_client.http.models import PointStruct
from Services.embeddings import get_embedding_model,get_embedding,embedding_dim
from Services.vector_store import ensure_collection, upsert_points, search
from pydantic import BaseModel
from typing import Optional

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    
logger=logging.getLogger('uvicorn.error')

data_Router=APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

@data_Router.post("/upload/{project_id}")
async def uploaFile(request:Request,project_id:str,file:UploadFile,AppSetting=Depends(getSettings)):
    
    Project_Model=ProjectModel(db_client=request.app.db_client)
    project=await Project_Model.get_project_or_create_one(project_id=project_id)
    
    IsValid,resultSignal=DataController().Validate_Uploaded_File(file=file)
    if  not IsValid :
         return JSONResponse(
             status_code=status.HTTP_400_BAD_REQUEST,
             content={
                 "Signal":resultSignal
             }
         )
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_Path,file_id=DataController().generate_unique_filepath(original_filename=file.filename,project_id=project_id)
       
    try:
            async with aiofiles.open(file_Path,"+wb")as f:
                while chunk:= await file.read(AppSetting.FILE_DEFAULT_CHUNKSIZE):
                    await f.write(chunk)
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
                 "Signal":Response_Signal.FILE_UPLOAD_SUCCESS.value,
                 "file_id":file_id,
                 "project_id":str(project._id)
             }
         )
    
@data_Router.post("/process/{project_id}")
async def Process_Endpoint(request:Request,project_id:str,Process_Request:Process_Request):
    file_id=Process_Request.file_id
    chunk_size=Process_Request.chunk_size
    overlap_size=Process_Request.overlap_size
    Do_Reset=Process_Request.Do_Reset
    
    
    Project_Model=ProjectModel(db_client=request.app.db_client)
    project=await Project_Model.get_project_or_create_one(project_id=project_id)
    
    Process_Controller=ProcessController(project_id=project_id)   
    file_content=Process_Controller.get_file_content(file_id=file_id)   
    file_chunks=Process_Controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size,
    )
    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
             status_code=status.HTTP_400_BAD_REQUEST,
             content={
                 "Signal":Response_Signal.PROCESSING_FAILED
             }
         )
    file_chunks_record=[
        
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project._id,
        )
        for i, chunk in enumerate(file_chunks)
    ]
    chunk_Model=ChunkModel(db_client=request.app.db_client)
    if Do_Reset==1:
        
        _=await chunk_Model.delete_chunks_by_projectId(project_id=project._id)
        
    
    inserted_ids = await chunk_Model.insert_chunks_in_batches(file_chunks_record)
    embeddings_points = []
    for chunk in file_chunks_record:
        
        vector = get_embedding(chunk.chunk_text)
        embeddings_points.append(
            
            PointStruct(
                
                id=chunk.chunk_order,
                vector=vector,
                payload={
                    
                    "text": chunk.chunk_text,
                    "metadata": chunk.chunk_metadata,
                    "project_id": str(project._id)
                }
            )
        )
    ensure_collection()
    upsert_points(embeddings_points)
    inserted_ids_str = [str(_id) for _id in inserted_ids]
    return JSONResponse(
            
             content={
                 "Signal":Response_Signal.PROCESSING_SUCCESS.value,
                 "Inserted_ids_str":inserted_ids_str,
             }
         )
    
@data_Router.post("/search/{project_id}")
async def search_chunks(project_id: str, search_request: SearchRequest):
    query_vector = get_embedding(search_request.query)
    COLLECTION_NAME=ensure_collection()
    results = search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        top_k=search_request.top_k,
        filter={"must": [{"key": "project_id", "match": {"value": project_id}}]}  
    )
    response = []
    for r in results:
        response.append({
            "text": r.payload.get("text"),
            "metadata": r.payload.get("metadata"),
            "score": r.score
        })
    
    return response
    
        
    
   