from pydantic_settings import BaseSettings,SettingsConfigDict
class settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    OPENAI_API_KEY:str
    FILE_ALLOWED_TYPES:list
    FILE_MAX_SIZE:int
    FILE_DEFAULT_CHUNKSIZE:int
    MONGODB_URL:str
    MONGODB_DATABASE:str
    qdrant_host: str
    qdrant_port: int
    qdrant_collection: str
    embedding_model: str
    
    class Config:
        env_file= ".env"

def getSettings():
    return settings()
        