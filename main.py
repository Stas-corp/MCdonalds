import uvicorn

from app.app import app

if __name__ == "__main__":
    uvicorn.run('main:app', reload=True, host='localhost')