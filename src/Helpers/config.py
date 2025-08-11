from pydantic_settings import BaseSettings,SettingsConfigDict
class settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str
    FILE_ALLOWED_TYPES:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNKSIZE:int
    
    class Config:
        env_file= ".env"

def getSettings():
    return settings()
        