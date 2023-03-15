import asyncio
import hashlib
import os
import shutil
import subprocess
import uuid

import yaml
from starlette.responses import FileResponse

from db.queries import get_file_from_db, get_hash_from_db, update_compile_test_in_db, delete_file_from_db
from settings import UPLOADED_FILES_PATH, COMPILE_DIR


# def format_filename(file, file_name):
#     # Split filename and extention
#     filename, ext = os.path.splitext(file.filename)
#     filename = str(file_name)
#     return filename + ext


async def save_file_to_uploads(request):
    req = await request.json()
    file_name = str(uuid.uuid4())
    yaml_text = yaml.dump(req)
    with open(f"{UPLOADED_FILES_PATH}{file_name}.yaml", "w") as file:
        file.write(yaml_text)
    return file_name
    # with open(f'{UPLOADED_FILES_PATH}{file_name}.yaml', "wb") as uploaded_file:
    #     file_content = await file.read()
    #     uploaded_file.write(file_content)
    #     uploaded_file.close()


def get_hash_md5(file_name):
    with open(f"{UPLOADED_FILES_PATH}{file_name}.yaml", 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def command_compil(file_name):
    cmd = f"esphome compile {UPLOADED_FILES_PATH}{file_name}.yaml"
    return cmd


async def compile_yaml_file(db, hash_yaml, name_esphome, file_name):
    old_file_info_from_db = get_hash_from_db(db, hash_yaml)
    if old_file_info_from_db is None:

        cmd = command_compil(file_name)

        subprocess.run(cmd)

        update_compile_test_in_db(db, file_name)

        shutil.copy2(f"{UPLOADED_FILES_PATH}.esphome/build/{name_esphome}/.pioenvs/{name_esphome}/firmware.bin",
                     f"{COMPILE_DIR}{file_name}.bin")

        # os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
    else:
        file_info_from_db = get_file_from_db(db, file_name)
        # os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')
        delete_file_from_db(db, file_info_from_db)


async def _read_stream(stream):
    while True:
        line = stream.readline()
        if line:
            linen = f'{line}\n\n'
            yield linen
        else:
            break