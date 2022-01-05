import traceback

import utils.processor as data_processor
from utils.logger import error_log, info_log
from utils.environments import create_environments
from utils.database import push_new_document, create_connection

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()
env = create_environments()


@app.get('/')
def health_check():
    return {'status': 'OK'}


# noinspection PyBroadException
@app.post("/crawler-receiver/")
async def create_file(data_file: UploadFile = File(...)):
    try:
        file_uploaded = data_file.file.read()
        clean_data = data_processor.process_data(file_uploaded)
    except Exception as _:
        error_log.error(traceback.format_exc())
        return JSONResponse({
            "success": False,
            "message": "Cannot parse file"
        }, status_code=400)
    try:
        db_connection = create_connection()
        year = data_processor.parse_year_from_file_name(data_file.filename)
        for row in clean_data:
            row['year'] = year
            push_new_document(
                row, collection_name=env.database_university_collection, client_connection=db_connection
            )
        push_new_document(
            {'year': year, 'data': clean_data},
            collection_name=env.database_year_collection,
            client_connection=db_connection
        )
        db_connection.close()
    except Exception as _:
        error_log.error(traceback.format_exc())
        return JSONResponse({
            "success": False,
            "message": "There some error while upload data"
        }, status_code=500)
    info_log.info(f'Pushed/Update {len(clean_data)} row(s)')
    return JSONResponse({
        "success": True
    }, status_code=200)
