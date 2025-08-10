from fastapi import FastAPI,APIRouter
import os
base_Router=APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)
@base_Router.get("/")
def welecome():
    App_name=os.getenv('APP_NAME')
    App_version=os.getenv('APP_VERSION')
    return{
        "App_name":App_name,
        "App_Version":App_version,
    }