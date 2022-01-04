import uvicorn
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.get('/')
def health_check():
    return {'status': 'OK'}


@app.post("/crawler-receiver/")
async def create_file(data_file: UploadFile = File(...)):
    print('123')
    print(data_file.file.read())
    return {
        "file_size": 1
    }
