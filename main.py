import os
import shutil
import subprocess
import uuid

import yaml
from fastapi import FastAPI, status, File, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from db import models
from db.connect import SessionLocal, engine
from lib.methods import format_filename, save_file_to_uploads, get_hash_md5, command_compil
from db.queries import add_file_to_db, get_file_from_db, get_hash_from_db, update_compile_test_in_db, \
    delete_file_from_db
from settings import UPLOADED_FILES_PATH, COMPILE_DIR

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/upload", tags=["Upload"], status_code=status.HTTP_200_OK)
async def upload_file(file: UploadFile = File(...),
                      db: Session = Depends(get_db)):
    #переименовую и сохраняю в папку
    file_name = str(uuid.uuid4())
    full_name = format_filename(file, file_name)
    await save_file_to_uploads(file, full_name)

    #читаю файл и достаю esphome name
    read_yaml = yaml.safe_load(open(f"{UPLOADED_FILES_PATH}{full_name}"))
    name_esphome = read_yaml['esphome']['name']

    #генерирую хеш и все добавляю в базу данных
    hash_yaml = get_hash_md5(full_name)
    data = add_file_to_db(db, file_name=file_name, name_esphome=name_esphome, hash_yaml=hash_yaml, compile_test=False)
    return data.id


@app.post("/compile", tags=["Compile"], status_code=status.HTTP_200_OK)
async def upload_file(
        id: int,
        db: Session = Depends(get_db)
):
    #получаю информацию из бд по id ищу скомпилированных хэш если был, компилирую или вывожу файл
    file_info_from_db = get_file_from_db(db, id)
    file_name = file_info_from_db.name_yaml
    name_esphome = file_info_from_db.name_esphome
    hash_yaml = file_info_from_db.hash_yaml

    new_file_info_from_db = get_hash_from_db(db, hash_yaml)
    if new_file_info_from_db is None:

        cmd = command_compil(db, id)
        subprocess.run(cmd)

        update_compile_test_in_db(db, id)

        shutil.copy2(f"{UPLOADED_FILES_PATH}.esphome/build/{name_esphome}/.pioenvs/{name_esphome}/firmware.bin",
                     f"{COMPILE_DIR}{file_name}.bin")

        os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
        return FileResponse(f"compile_files/{file_name}.bin",
                            filename=f"{file_name}.bin",
                            media_type="application/octet-stream")
    else:
        os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
        delete_file_from_db(db, file_info_from_db)
        file_name = new_file_info_from_db.name_yaml
        return FileResponse(f"compile_files/{file_name}.bin",
                            filename=f"{file_name}.bin",
                            media_type="application/octet-stream")


@app.post("/logs", tags=["Logs"], status_code=status.HTTP_200_OK)
async def upload_file(
        id: int,
        db: Session = Depends(get_db)
):
    cmd = command_compil(db, id)

    logs = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, stderr = logs.communicate()

    return stdout
