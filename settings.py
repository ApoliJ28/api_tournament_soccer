from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    title_project:str = 'Tournament Soccer API'
    debug:bool = True
    version:str = '1.0.0'
    descripcion_app:str = 'Application of a forum soccer tournament...'
    author:str = 'Victor Apolinares - Develoment'
    
    host:str = os.getenv('HOST')
    port:int = int(os.getenv('PORT'))
    log_level:str = 'info'
    
    database_url :str = os.getenv('DATABASE_URL')
    
    secret_key:str = 'IMpm6idnZCgvlep1lUnvuBsmey3xqTFd'
    algorithm:str = 'HS256'
    
    class Config:
        env_file = '.env'
