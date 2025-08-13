from fastapi import FastAPI
from dotenv import load_dotenv

from Routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from Heplers import getSettings

app=FastAPI()
@app.on_event("startup")
async def startup_db_client():
    settings=getSettings()
    app.mongo_conn=AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongo_client=app.mongo_conn[settings.MONGODB_DATABASE]
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()

app.include_router(base.base_Router)
app.include_router(data.data_Router)
    
