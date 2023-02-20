import hashlib
import os

from db.queries import get_file_from_db
from settings import UPLOADED_FILES_PATH


async def save_file_to_uploads(file, filename):
    with open(f'{UPLOADED_FILES_PATH}{filename}', "wb") as uploaded_file:
        file_content = await file.read()
        uploaded_file.write(file_content)
        uploaded_file.close()


def format_filename(file, file_name):
    # Split filename and extention
    filename, ext = os.path.splitext(file.filename)
    filename = str(file_name)
    return filename + ext


def command_compil(db, id):
    file_info_from_db = get_file_from_db(db, id)
    file_name = file_info_from_db.name_yaml
    cmd = f"esphome compile {UPLOADED_FILES_PATH}{file_name}.yaml"
    return cmd


def get_hash_md5(full_name):
    with open(f"{UPLOADED_FILES_PATH}{full_name}", 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

