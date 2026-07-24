from pydantic_settings import BaseSettings, SettingsConfigDict
 
class Settings(BaseSettings):
   model_config = SettingsConfigDict(env_file=".env")

   APP_NAME: str
   DATABASE_URL: str
   AWS_REGION: str
   AWS_ACCESS_KEY_ID:str
   AWS_SECRET_ACCESS_KEY:str
   DATABASE_READY:str
   BEDROCK_MODEL_ID:str
   AWS_DEMO_MODE:str





settings = Settings()

