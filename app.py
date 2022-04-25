import uvicorn
from fastapi import FastAPI, Path

app = FastAPI()


@app.get('/')
def index():
    return {
        'server': 'up & running'
    }