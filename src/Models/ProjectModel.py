from .BaseDataModel import BaseDataModel
from .db_schemes.project import project
from Models.enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId

class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        
    async def create_project(self,Project_obj:project):
        result=await self.collection.insert_one(Project_obj.dict())
        Project_obj._id=result.inserted_id
        return Project_obj
    
    async def get_project_or_create_one(self,project_id:str):
        record=await self.collection.find_one({
            "project_id":project_id
        })
        if record is None:
            #create new project
            new_project=project(project_id=project_id)
            new_project=await self.create_project(Project_obj=new_project)
            return new_project
        proj = project(**record)
        proj._id = record["_id"]
        return proj
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        total_documents = await self.collection.count_documents({})
        total_pages = total_documents // page_size
        if total_documents % page_size>0:
            
            
            total_pages+=1
        
        skip_count = (page - 1) * page_size
        cursor = self.collection.find().skip(skip_count).limit(page_size)

        projects = []
        async for document in cursor:
            
            
            projects.append(project(**document))  

        return projects, total_pages
        
    
    
    