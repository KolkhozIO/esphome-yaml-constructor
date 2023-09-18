import hashlib
import os
import shutil
import re

import yaml

from db.dals import ConfigDAL, FavouritesDAL, GoogleDAL
from settings import UPLOADED_FILES_PATH, COMPILE_DIR, COMPILE_DIR_OTA


async def save_file_to_uploads(request, file_name):
    req = await request.json()
    yaml_text = yaml.dump(req)
    with open(f"{UPLOADED_FILES_PATH}{file_name}.yaml", "w") as file:
        file.write(yaml_text)


async def get_info_config(request):
    req = await request.json()
    yaml_text = yaml.dump(req)

    m = hashlib.md5()
    m.update(yaml_text.encode('utf-8'))
    hash_yaml = m.hexdigest()

    name_esphome = req['esphome'].get('name')

    if 'esp32' in req or req['esphome'].get('platform') == "ESP32":
        platform = "ESP32"
    else:
        platform = "ESP8266"

    return {
        "hash_yaml": hash_yaml,
        "name_esphome": name_esphome,
        "platform": platform
    }


async def get_hash_yaml(request):
    req = await request.json()
    yaml_text = yaml.dump(req)

    m = hashlib.md5()
    m.update(yaml_text.encode('utf-8'))
    return m.hexdigest()


def read_stream(stream):
    while True:
        line = stream.readline()
        if line:
            clean_line = re.sub(rb'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]', b'', line)
            clean_line = clean_line.decode('utf-8', errors='ignore').replace('\r', '').replace('\n', '')
            linen = f'{clean_line}\n\n'
            yield linen
        else:
            break


async def post_compile_process(file_name, db):
    info_config = await _execute_function(ConfigDAL,
                                          ConfigDAL.get_config,
                                          session=db,
                                          name_config=file_name)
    if not info_config.compile_test:
        await _execute_function(ConfigDAL,
                                ConfigDAL.update_yaml_config,
                                session=db,
                                name_config=file_name)
        shutil.copy2(
            f"{UPLOADED_FILES_PATH}.esphome/build/{info_config.name_esphome}/.pioenvs/{info_config.name_esphome}/firmware-factory.bin",
            f"{COMPILE_DIR}{file_name}.bin")
        shutil.copy2(
            f"{UPLOADED_FILES_PATH}.esphome/build/{info_config.name_esphome}/.pioenvs/{info_config.name_esphome}/firmware.bin",
            f"{COMPILE_DIR_OTA}{file_name}.bin")
    os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')


async def save_config_json(request, db):
    # save json and file name to database, create url and return it
    json_text = await request.json()
    name_esphome = json_text['esphome'].get('name')
    hash_yaml = await get_hash_yaml(request)

    info_old_config_json = await _execute_function(ConfigDAL,
                                                   ConfigDAL.get_config,
                                                   session=db,
                                                   hash_yaml=hash_yaml)
    await _execute_function(ConfigDAL,
                            ConfigDAL.get_config,
                            session=db,
                            hash_yaml=hash_yaml)
    if info_old_config_json is not None and info_old_config_json.config_json is not None:
        name_config = info_old_config_json.name_config
    elif info_old_config_json is not None and info_old_config_json.config_json is None:
        name_config = await _execute_function(ConfigDAL,
                                              ConfigDAL.update_config_json,
                                              session=db,
                                              hash_yaml=hash_yaml,
                                              config_json=json_text)
    else:
        new_config = await _execute_function(ConfigDAL,
                                             ConfigDAL.create_yaml_config,
                                             session=db,
                                             hash_yaml=hash_yaml,
                                             config_json=json_text)
        name_config = new_config.name_config
    return {"name_config": name_config, "name_esphome": name_esphome}


async def _execute_function(dal, func, session, *args, **kwargs):
    async with session.begin():
        return await func(dal(session), *args, **kwargs)
