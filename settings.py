from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    title_project:str = "Tournament Soccer API"
    debug:bool = False
    version:str = '1.0.0'
    
    host:str = os.getenv('HOST')
    port:int = int(os.getenv('PORT'))
    log_level:str = 'info'
