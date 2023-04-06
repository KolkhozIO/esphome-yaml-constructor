import asyncio
import os
import subprocess
import uuid

import yaml
from fastapi import FastAPI, status, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, JSONResponse
import uvicorn

from db import models
from db.connect import SessionLocal, engine
from lib.methods import save_file_to_uploads, get_hash_md5, command_compil, compile_yaml_file, _read_stream
from db.queries import add_file_to_db, get_hash_from_db, add_yaml_to_db, get_yaml_from_db, get_hash_from_db_in_logs
from settings import UPLOADED_FILES_PATH

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

origins = [os.environ.get('SERVER_API_URL')]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/share", tags=["Share"], status_code=status.HTTP_201_CREATED)
async def create_share_file(request: Request, db: Session = Depends(get_db)):
    req = await request.json()
    file_name = str(uuid.uuid4())
    yaml_text = yaml.dump(req)
    add_yaml_to_db(db, file_name, yaml_text)
    url = f"config-generator.com/config/{file_name}"
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'uuid': file_name,
            'url': url
        }
    )


@app.get("/share/{uuid}", tags=["Share"], status_code=status.HTTP_200_OK)
async def get_share_file(file_name: str, db: Session = Depends(get_db)):
    info_file = get_yaml_from_db(db, file_name)
    json_info_file = jsonable_encoder(info_file)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=json_info_file['yaml_text']
    )


@app.post("/upload", tags=["Upload"], status_code=status.HTTP_200_OK)
async def upload_file(request: Request, db: Session = Depends(get_db)):
    # переименовую и сохраняю в папку
    file_name = await save_file_to_uploads(request)

    # читаю файл и достаю esphome name
    read_yaml = yaml.safe_load(open(f"{UPLOADED_FILES_PATH}{file_name}.yaml"))
    name_esphome = read_yaml['esphome']['name']

    # генерирую хеш и все добавляю в базу данных
    hash_yaml = get_hash_md5(file_name)
    old_file_info_from_db = get_hash_from_db(db, hash_yaml)
    if old_file_info_from_db is None:
        file_info_from_db = add_file_to_db(db, file_name=file_name, name_esphome=name_esphome, hash_yaml=hash_yaml,
                                           compile_test=False)
        print(file_info_from_db.name_yaml)
        # компилирую yaml файл и сохраняю в папку compile_files в фоновом режиме
        asyncio.create_task(compile_yaml_file(db, hash_yaml, name_esphome, file_name))
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=hash_yaml
    )


@app.post("/compile", tags=["Compile"], status_code=status.HTTP_200_OK)
async def compile_file(
        hash_yaml: str,
        db: Session = Depends(get_db)
):
    # получаю информацию о файле, удаляю yaml файл, возвращаю бинарник пользователю

    file_info_from_db = get_hash_from_db(db, hash_yaml)
    file_name = file_info_from_db.name_yaml
    os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
    return FileResponse(f"compile_files/{file_name}.bin",
                        filename=f"{file_name}.bin",
                        media_type="application/octet-stream")


@app.get("/logs", tags=["Logs"], status_code=status.HTTP_200_OK)
async def logs_compile_file(
        hash_yaml: str,
        db: Session = Depends(get_db)
):
    # получаю информацию о файле из бд
    file_info_from_db = get_hash_from_db_in_logs(db, hash_yaml)
    file_name = file_info_from_db.name_yaml
    # cmd - комманда выполнения компиляции
    cmd = command_compil(file_name)
    # процесс компиляции
    process = await asyncio.to_thread(subprocess.Popen, cmd,
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # построчный вывод логов(генератор)
    otv = _read_stream(process.stdout)
    return StreamingResponse(otv)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
