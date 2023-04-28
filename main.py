import asyncio
import os
import subprocess
import uuid

import uvicorn
import yaml
from fastapi import FastAPI, status, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse

from db import models
from db.connect import SessionLocal, engine
from db.queries import add_file_to_db, get_hash_from_db, add_yaml_to_db, get_yaml_from_db
from lib.methods import save_file_to_uploads, get_hash_md5, command_compil, compile_yaml_file, read_stream
from settings import UPLOADED_FILES_PATH

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

origins = [os.environ.get('APP_URL')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/share", tags=["Share"], status_code=status.HTTP_201_CREATED)
async def create_share_file(request: Request, db: Session = Depends(get_db)):
    # save json and file name to database, create url and return it
    json_text = await request.json()
    file_name = str(uuid.uuid4())
    add_yaml_to_db(db, file_name, json_text)
    url_front = os.environ.get('APP_URL')
    url = f"{url_front}/config?uuid={file_name}"
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'uuid': file_name,
            'url': url
        }
    )


@app.get("/share", tags=["Share"], status_code=status.HTTP_200_OK)
async def get_share_file(file_name=str, db: Session = Depends(get_db)):
    # fetches json from database and returns it
    info_file = get_yaml_from_db(db, file_name)
    json_info_file = jsonable_encoder(info_file)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={'json_text': json_info_file['json_text']}
    )


@app.post("/validate", tags=["Validate"], status_code=status.HTTP_200_OK)
async def validate(
    request: Request,
    db: Session = Depends(get_db)
):
    file_name = await save_file_to_uploads(request)
    # cmd - compile command
    cmd = f"esphome logs {UPLOADED_FILES_PATH}{file_name}.yaml"
    # compilation process
    process = await asyncio.to_thread(subprocess.Popen, cmd,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # line-by-line output of logs (generator)
    otv = read_stream(process.stdout)
    # deleting the created yaml file
    os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
    return StreamingResponse(otv)


@app.post("/compile", tags=["Compile"], status_code=status.HTTP_200_OK)
async def compile_file(request: Request, db: Session = Depends(get_db)):
    # rename and save to a folder
    file_name = await save_file_to_uploads(request)

    # read file and get esphome name
    read_yaml = yaml.safe_load(open(f"{UPLOADED_FILES_PATH}{file_name}.yaml"))
    name_esphome = read_yaml['esphome']['name']

    # generate a hash and add everything to the database
    hash_yaml = get_hash_md5(file_name)
    old_file_info_from_db = get_hash_from_db(db, hash_yaml)
    if old_file_info_from_db is None:
        file_info_from_db = add_file_to_db(db, name_yaml=file_name, name_esphome=name_esphome, hash_yaml=hash_yaml,
                                           compile_test=False)
        print(file_info_from_db.name_yaml)
        # compile the yaml file and save it to the compile_files folder in the background
        asyncio.create_task(compile_yaml_file(db, name_esphome, file_name))
    cmd = command_compil(file_name)
    process = await asyncio.to_thread(subprocess.Popen, cmd,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # line-by-line output of logs (generator)
    otv = read_stream(process.stdout)
    return StreamingResponse(otv)


@app.post("/download", tags=["Download"], status_code=status.HTTP_200_OK)
async def download_bin(
        request: Request,
        db: Session = Depends(get_db)
):
    # get information about the file, delete the yaml file, return the binary to the user
    file_name = await save_file_to_uploads(request)
    hash_yaml = get_hash_md5(file_name)
    os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
    file_info_from_db = get_hash_from_db(db, hash_yaml)
    file_name = file_info_from_db.name_yaml
    os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
    return FileResponse(f"compile_files/{file_name}.bin",
                        filename=f"{file_name}.bin",
                        media_type="application/octet-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
