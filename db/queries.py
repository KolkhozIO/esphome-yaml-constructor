from db import models


def add_file_to_db(db, **kwargs):
    new_file = models.Filename(name_yaml=kwargs['file_name'], name_esphome=kwargs['name_esphome'],
                                  hash_yaml=kwargs['hash_yaml'])
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def get_file_from_db(db, file_name):
    return db.query(models.Filename).filter(models.Filename.name_yaml == file_name).first()


def get_hash_from_db(db, hash_yaml):
    return db.query(models.Filename).filter(models.Filename.hash_yaml == hash_yaml,
                                               models.Filename.compile_test == True).first()


def update_compile_test_in_db(db, file_name):
    update_file = get_file_from_db(db, file_name)
    update_file.compile_test = True

    db.commit()
    db.refresh(update_file)
    return update_file


def delete_file_from_db(db, file_info_from_db):
    db.delete(file_info_from_db)
    db.commit()


def add_yaml_to_db(db, file_name, yaml_text):
    new_file = models.Yamlfile(uuid=file_name, yaml_text=yaml_text)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file


def get_yaml_from_db(db, file_name):
    return db.query(models.Yamlfile).filter(models.Yamlfile.uuid == file_name).first()
