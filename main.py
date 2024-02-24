import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import router as main_router

app = FastAPI(docs_url='/api/docs', redoc_url='/api/redoc', openapi_url='/api/openapi.json')

origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:3000',
    'http://89.223.30.75:80'
    'https://89.223.30.75',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(main_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
