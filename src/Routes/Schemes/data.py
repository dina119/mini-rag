from pydantic import BaseModel
from typing import Optional

class Process_Request(BaseModel):
    file_id:str
    chunk_size:Optional[int]=100
    overlap_size:Optional[int]=20
    Do_Reset:Optional[int]=0
