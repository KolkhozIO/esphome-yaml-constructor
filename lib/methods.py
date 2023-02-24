import hashlib
import os
import uuid

import yaml

from db.queries import get_file_from_db
from settings import UPLOADED_FILES_PATH


async def save_file_to_uploads(request):
    req = await request.json()
    file_name = str(uuid.uuid4())
    yaml_text = yaml.dump(req)
    with open(f"{UPLOADED_FILES_PATH}{file_name}.yaml", "w") as file:
        file.write(yaml_text)
    return file_name


def command_compil(db, id):
    file_info_from_db = get_file_from_db(db, id)
    file_name = file_info_from_db.name_yaml
    cmd = f"esphome compile {UPLOADED_FILES_PATH}{file_name}.yaml"
    return cmd


def get_hash_md5(file_name):
    with open(f"{UPLOADED_FILES_PATH}{file_name}.yaml", 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

