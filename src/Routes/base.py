from fastapi import FastAPI,APIRouter,Depends
from Helpers.config import getSettings

base_Router=APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)
@base_Router.get("/")
async def welecome(AppSetting=Depends(getSettings)):
     App_name=AppSetting.APP_NAME
     App_version=AppSetting.APP_VERSION
     return{
        "App_name":App_name,
        "App_Version":App_version,
    }