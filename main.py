import os
import shutil
import subprocess
import uuid
from fileinput import filename

import yaml
from fastapi import FastAPI, Response, status, File, UploadFile, Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

import db_models
from db_connect import SessionLocal, engine
from methods import format_filename, save_file_to_uploads, add_file_to_db, get_file_from_db
from settings import UPLOADED_FILES_PATH, COMPILE_DIR

db_models.Base.metadata.create_all(engine)


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
    file_name = str(uuid.uuid4())
    full_name = format_filename(file, file_name)
    await save_file_to_uploads(file, full_name)
    read_yaml = yaml.safe_load(open(f"{UPLOADED_FILES_PATH}{full_name}"))
    name_esphome = read_yaml['esphome']['name']
    data = add_file_to_db(db, file_name=file_name, name_esphome=name_esphome)

    return data.id


@app.post("/compile", tags=["Compile"], status_code=status.HTTP_200_OK)
async def upload_file(
        id: int,
        db: Session = Depends(get_db)
):
    file_info_from_db = get_file_from_db(db, id)
    file_name = file_info_from_db.name_yaml
    name_esphome = file_info_from_db.name_esphome
    cmd = f"esphome compile {UPLOADED_FILES_PATH}{file_name}.yaml"
    subprocess.run(cmd)
    shutil.copy2(f"{UPLOADED_FILES_PATH}.esphome/build/{name_esphome}/.pioenvs/{name_esphome}/firmware.bin",
                 f"{COMPILE_DIR}{file_name}.bin")
    os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
    return FileResponse(f"compile_files/{file_name}.bin",
                        filename=f"{file_name}.bin",
                        media_type="application/octet-stream")


@app.post("/logs", tags=["Logs"], status_code=status.HTTP_200_OK)
async def upload_file(
        id: int,
        db: Session = Depends(get_db)
):
    file_info_from_db = get_file_from_db(db, id)
    file_name = file_info_from_db.name_yaml
    cmd = f"esphome compile {UPLOADED_FILES_PATH}{file_name}.yaml"

    # returned_output = subprocess.check_output(cmd)
    # logs = returned_output.decode("utf-8")

    # try:
    #     logs = subprocess.check_output(
    #         cmd,
    #         stderr=subprocess.STDOUT,
    #     ).decode("utf-8")
    #
    # except subprocess.CalledProcessError as e:
    #     logs = str(e)

    # logs = subprocess.check_output(
    #     cmd,
    #     stderr=subprocess.STDOUT,
    #     shell=True).output()

    logs = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, stderr = logs.communicate()

    return stdout
