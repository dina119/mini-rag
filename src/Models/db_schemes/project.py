from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId
class project(BaseModel):
    _id: Optional[ObjectId]=None
    project_id:str=Field(...,min_length=1)
    
    @validator('project_id')
    def validate_project_id(cls,value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumirc")
        return value
    
    class Config:
        arbitrary_types_allowed=True
        
    @classmethod
    def get_indexes(cls):
        return[
            {
              "key":
                ("project_id",1),
             "name":"project_id_index_1",
             "unique":True
             
            }
        ]
        
    
    