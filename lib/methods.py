import asyncio
import hashlib
import shutil
import subprocess
import uuid
import re

import yaml

from db.queries import update_compile_test_in_db
from settings import UPLOADED_FILES_PATH, COMPILE_DIR


async def save_file_to_uploads(request):
    req = await request.json()
    file_name = str(uuid.uuid4())
    yaml_text = yaml.dump(req)
    with open(f"{UPLOADED_FILES_PATH}{file_name}.yaml", "w") as file:
        file.write(yaml_text)
    return file_name


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
    cmd = ['esphome', 'compile', f'{UPLOADED_FILES_PATH}{file_name}.yaml']
    return cmd


async def compile_yaml_file(db, name_esphome, file_name):
    cmd = command_compil(file_name)
    process = subprocess.Popen(cmd)
    await asyncio.to_thread(process.wait)
    update_compile_test_in_db(db, file_name)

    shutil.copy2(f"{UPLOADED_FILES_PATH}.esphome/build/{name_esphome}/.pioenvs/{name_esphome}/firmware.bin",
                 f"{COMPILE_DIR}{file_name}.bin")


def read_stream(process):
    while True:
        line = process.stdout.readline()
        if line:
            clean_line = re.sub(rb'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', b'', line)
            clean_line = clean_line.decode().replace('\r', '').replace('\n', '')
            linen = f'{clean_line}\n\n'
            yield linen
        else:
            break


def get_hash_validate(yaml_text):
    with yaml_text as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def save_file_to_validate(request):
    req = request.query_params.get('yaml_text')
    file_name = str(uuid.uuid4())
    yaml_text = yaml.dump(req)
    with open(f"{UPLOADED_FILES_PATH}{file_name}.yaml", "w") as file:
        file.write(yaml_text)
    return file_name


async def post_compile_process(old_file_info_from_db, file_name, name_esphome, db):
    if old_file_info_from_db is None:
        update_compile_test_in_db(db, file_name)
        shutil.copy2(f"{UPLOADED_FILES_PATH}.esphome/build/{name_esphome}/.pioenvs/{name_esphome}/firmware.bin",
                     f"{COMPILE_DIR}{file_name}.bin")
