import uvicorn
from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI()
    return app

if __name__ == '__main__':
    uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)
