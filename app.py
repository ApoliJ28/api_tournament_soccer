from fastapi import FastAPI, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from settings import Settings
from routes import user, auth

setting = Settings()

app = FastAPI(title=setting.title_project, version=setting.version)

app.include_router(auth.router)
app.include_router(user.router)

@app.get('/', status_code=status.HTTP_200_OK, include_in_schema=True)
async def index():
    return {
        'description': setting.descripcion_app,
        'author': setting.author
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

if __name__ == '__main__':
    
    uvicorn.run('app:app',host=setting.host, port=setting.port, log_level=setting.log_level, reload=setting.debug)
