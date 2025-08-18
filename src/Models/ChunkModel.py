from .BaseDataModel import BaseDataModel
from .db_schemes.dataChunk import DataChunk
from Models.enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
from pymongo import InsertOne
from typing import List

class ChunkModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
    
    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        
        self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
        indexes=DataChunk.get_indexes()
        for index in indexes:
            
            try:
                    await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )
            except Exception as e:
                print(f"Failed to create index {index['name']}: {e}")
                    
                
    
    async def create_chunk(self,chunk:DataChunk):
        result=await self.collection.insert_one(chunk.dict())
        chunk._id=result.inserted_id
        return chunk
    
    async def get_chunk(self,chunk_id:str):
        result= await self.collection.find_one({
            "_id":ObjectId(chunk_id)
        })
        if result is None :
            return None
        return DataChunk(**result)
    
    # async def insert_many_chunks(self,chunks:list,batch_size:int=100):
    #     for i in range (0,len(chunks),batch_size):
    #         batch=chunks[i:batch_size+i]
    #         operations=[
    #             InsertOne(chunk.dict())
    #             for chunk in batch  
    #         ]
    #         await self.collection.bulk_write(operations)
    #     return len(chunks)
    
    async def insert_chunks_in_batches(self, chunks, batch_size=1000):
        
        all_ids = []
        for i in range(0, len(chunks), batch_size):
            
            batch = chunks[i:i+batch_size]
            result =await self.collection.insert_many([chunk.dict() for chunk in batch])
            all_ids.extend(result.inserted_ids)
        return all_ids

    
    async def delete_chunks_by_projectId(self,project_id:ObjectId):
        result=await self.collection.delete_many({
            "chunk_project_id":project_id
        })
        return result.deleted_count
    
    async def get_chunks_by_projectId(self, project_id: ObjectId) -> List[DataChunk]:
        cursor = self.collection.find({"chunk_project_id": project_id}).sort("chunk_order", 1)
        results = []
        async for doc in cursor:
            results.append(DataChunk(**doc))
        return results
        