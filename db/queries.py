from db import models


def add_file_to_db(db, **kwargs):
    new_file = models.Filename(name_yaml=kwargs['file_name'], name_esphome=kwargs['name_esphome'],
                                  hash_yaml=kwargs['hash_yaml'])
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def get_file_from_db(db, id):
    return db.query(models.Filename).filter(models.Filename.id == id).first()


def get_hash_from_db(db, hash_yaml):
    return db.query(models.Filename).filter(models.Filename.hash_yaml == hash_yaml,
                                               models.Filename.compile_test == True).first()


def update_compile_test_in_db(db, id):
    update_file = get_file_from_db(db, id)
    update_file.compile_test = True

    db.commit()
    db.refresh(update_file)
    return update_file


def delete_file_from_db(db, file_info_from_db):
    db.delete(file_info_from_db)
    db.commit()
