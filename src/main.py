from fastapi import FastAPI
from dotenv import load_dotenv

from Routes import base,data


app=FastAPI()
app.include_router(base.base_Router)
app.include_router(data.data_Router)
    
