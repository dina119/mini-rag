from pydantic import BaseModel,Field,validator
from typign import optional
from bson.objectid import ObjectId
class project(BaseModel):
    _id: optional[ObjectId]
    project_id:str=Field(...,min_length=1)
    
    @validator('project_id')
    def validate_project_id(cls,value):
        if not value.isalnum():
            raise ValueError("project_id must be alphanumirc")
        return value
    
    class config:
        arbitary_types_allowed=true
        
    
    