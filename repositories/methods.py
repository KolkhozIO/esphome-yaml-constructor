import os

from db import db_models
from repositories.settings import UPLOADED_FILES_PATH


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


def add_file_to_db(db, **kwargs):
    new_file = db_models.Filename(name_yaml=kwargs['file_name'], name_esphome=kwargs['name_esphome'])
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def get_file_from_db(db, id):
    return db.query(db_models.Filename).filter(db_models.Filename.id == id).first()
