from fastapi import FastAPI, status
import uvicorn
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(debug=True)

@app.get('/', status_code=status.HTTP_200_OK, include_in_schema=True)
async def index():
    return {
        'description': "Application of a forum soccer tournament...",
        'author': 'Victor Apolinares - Develoment'
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

if __name__ == '__main__':
    
    uvicorn.run('app:app',host=os.getenv('HOST'), port=int(os.getenv('PORT')), log_level='info', reload=True)