import hashlib
import os
import shutil
import re

import yaml
from lib.config import _get_yamlconfig_by_nameyaml, _update_yaml_config, _get_config_by_config_json, \
    _get_config_by_hash, _update_config_json, _create_new_json
from settings import UPLOADED_FILES_PATH, COMPILE_DIR


async def save_file_to_uploads(request, file_name):
    req = await request.json()
    print(req)
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
    info_config = await _get_yamlconfig_by_nameyaml(name_config=file_name, session=db)
    if not info_config.compile_test:
        await _update_yaml_config(name_config=file_name, session=db)
        shutil.copy2(
            f"{UPLOADED_FILES_PATH}.esphome/build/{info_config.name_esphome}/.pioenvs/{info_config.name_esphome}/firmware-factory.bin",
            f"{COMPILE_DIR}{file_name}.bin")
    os.remove(f'{UPLOADED_FILES_PATH}{file_name}.yaml')


async def save_config_json(request, db):
    # save json and file name to database, create url and return it
    json_text = await request.json()
    name_esphome = json_text['esphome'].get('name')
    hash_yaml = await get_hash_yaml(request)

    info_old_config_json = await _get_config_by_config_json(hash_yaml=hash_yaml, session=db)
    if info_old_config_json is not None:
        name_config = info_old_config_json.name_config
    else:
        info_old_hash = await _get_config_by_hash(hash_yaml=hash_yaml, session=db)
        if info_old_hash is not None:
            name_config = await _update_config_json(hash_yaml=hash_yaml, config_json=json_text, session=db)
        else:
            new_config = await _create_new_json(hash_yaml=hash_yaml, config_json=json_text, session=db)
            name_config = new_config.name_config
    return {"name_config": name_config, "name_esphome": name_esphome}
