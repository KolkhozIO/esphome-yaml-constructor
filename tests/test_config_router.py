import json
import os
from uuid import UUID, uuid4

from settings import UPLOADED_FILES_PATH, COMPILE_DIR
from tests.conftest import get_file_name, get_hash_config
from tests.settings_tests import config_data, config_failed_data


async def test_validate_endpoint(client):
    resp = client.post("/validate", data=json.dumps(config_data))
    data_from_resp = resp.text

    assert resp.status_code == 200
    assert "Configuration is valid!" in data_from_resp

    file_name = get_file_name(data_from_resp)
    uploaded_file_path = f'{UPLOADED_FILES_PATH}{file_name}.yaml'
    assert not os.path.exists(uploaded_file_path)


async def test_failed_validate_endpoint(client):
    resp = client.post("/validate", data=json.dumps(None))
    data_from_resp = resp.text

    assert resp.status_code == 200
    assert "Failed config" in data_from_resp

    file_name = get_file_name(data_from_resp)
    uploaded_file_path = f'{UPLOADED_FILES_PATH}{file_name}.yaml'
    assert not os.path.exists(uploaded_file_path)


async def test_save_config_endpoint(client, get_config_from_database):
    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp = resp.json()
    config_from_db = await get_config_from_database(data_from_resp["name_config"])

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 200
    assert config_from_db["name_config"] == UUID(data_from_resp["name_config"])
    assert config_from_db["hash_yaml"] == get_hash_config(config_data)
    assert config_from_db["name_esphome"] == "edfhgkd"
    assert config_from_db["platform"] == "ESP32"
    assert os.path.exists(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')
    os.remove(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')
    assert not os.path.exists(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')


async def test_save_config_if_compile_false(client, create_config_in_database, get_config_by_config_json, get_config_from_database):
    create_config_data = {
        "name_config": uuid4(),
        "hash_yaml": "205d5758d4cc066603a617faf6ad7c29",
        "name_esphome": None,
        "platform": None,
        "compile_test": False,
        "config_json": json.dumps(config_data),
    }

    await create_config_in_database(**create_config_data)
    create_config_in_db = await get_config_by_config_json(json.dumps(config_data))
    assert len(create_config_in_db) == 1
    create_config_in_db = dict(create_config_in_db[0])

    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp = resp.json()
    config_from_db = await get_config_from_database(data_from_resp["name_config"])

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 200
    assert create_config_in_db["name_config"] == UUID(data_from_resp["name_config"])
    assert create_config_in_db["name_config"] == config_from_db["name_config"]
    assert create_config_in_db["hash_yaml"] == get_hash_config(config_data)
    assert create_config_in_db["hash_yaml"] == config_from_db["hash_yaml"]
    assert create_config_in_db["name_esphome"] != config_from_db["name_esphome"]
    assert create_config_in_db["platform"] != config_from_db["platform"]
    assert create_config_in_db["compile_test"] == config_from_db["compile_test"]
    assert create_config_in_db["config_json"] == config_from_db["config_json"]
    assert os.path.exists(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')
    os.remove(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')
    assert not os.path.exists(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')


async def test_save_config_if_compile_true(client, get_config_from_database, get_config_by_config_json,
                                           create_config_in_database):
    create_config_data = {
        "name_config": uuid4(),
        "hash_yaml": "205d5758d4cc066603a617faf6ad7c29",
        "name_esphome": "name",
        "platform": "platform",
        "compile_test": True,
        "config_json": json.dumps(config_data),
    }

    await create_config_in_database(**create_config_data)
    create_config_in_db = await get_config_by_config_json(json.dumps(config_data))
    assert len(create_config_in_db) == 1
    create_config_in_db = dict(create_config_in_db[0])

    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp = resp.json()
    config_from_db = await get_config_from_database(data_from_resp["name_config"])

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 200
    assert create_config_in_db["name_config"] == UUID(data_from_resp["name_config"])
    assert create_config_in_db["name_config"] == config_from_db["name_config"]
    assert create_config_in_db["hash_yaml"] == get_hash_config(config_data)
    assert create_config_in_db["hash_yaml"] == config_from_db["hash_yaml"]
    assert create_config_in_db["name_esphome"] == config_from_db["name_esphome"]
    assert create_config_in_db["platform"] == config_from_db["platform"]
    assert create_config_in_db["compile_test"] == config_from_db["compile_test"]
    assert create_config_in_db["config_json"] == config_from_db["config_json"]
    assert os.path.exists(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')
    os.remove(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')
    assert not os.path.exists(f'{UPLOADED_FILES_PATH}{data_from_resp["name_config"]}.yaml')


async def test_failed_save_config_endpoint(client):
    resp = client.post("/save_config", data=json.dumps(None))
    data_from_resp = resp.json()

    assert resp.status_code == 404
    assert data_from_resp['detail'] == 'Item not found'


async def test_compile_endpoint(client, get_config_from_database):
    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp = resp.json()
    name_config = data_from_resp["name_config"]
    assert os.path.exists(f'{UPLOADED_FILES_PATH}{name_config}.yaml')

    resp = client.post("/compile", data=name_config)
    config_from_db = await get_config_from_database(name_config)
    data_from_resp = resp.text

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 200
    assert resp.headers == [(b'content-type', b'text/event-stream; charset=utf-8')]
    assert "INFO Successfully compiled program." in data_from_resp
    assert get_file_name(data_from_resp) == str(config_from_db["name_config"])
    assert os.path.exists(
        f'{UPLOADED_FILES_PATH}.esphome/build/{config_from_db["name_esphome"]}/.pioenvs/{config_from_db["name_esphome"]}/firmware-factory.bin')
    assert os.path.exists(f'{COMPILE_DIR}{str(config_from_db["name_config"])}.bin')
    assert not os.path.exists(f'{UPLOADED_FILES_PATH}{str(config_from_db["name_config"])}.yaml')
    os.remove(f'{COMPILE_DIR}{str(config_from_db["name_config"])}.bin')


async def test_compile_endpoint_two(client, get_config_from_database):
    resp = client.post("/save_config", data=json.dumps(config_failed_data))
    data_from_resp = resp.json()
    name_config = data_from_resp["name_config"]
    assert os.path.exists(f'{UPLOADED_FILES_PATH}{name_config}.yaml')

    resp = client.post("/compile", data=name_config)
    config_from_db = await get_config_from_database(name_config)
    data_from_resp = resp.text

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 200
    assert resp.headers == [(b'content-type', b'text/event-stream; charset=utf-8')]
    assert "Failed config" in data_from_resp
    assert get_file_name(data_from_resp) == str(config_from_db["name_config"])
    assert not os.path.exists(
        f'{UPLOADED_FILES_PATH}.esphome/build/{config_from_db["name_esphome"]}/.pioenvs/{config_from_db["name_esphome"]}/firmware-factory.bin')
    assert not os.path.exists(f'{COMPILE_DIR}{str(config_from_db["name_config"])}.bin')
    assert os.path.exists(f'{UPLOADED_FILES_PATH}{str(config_from_db["name_config"])}.yaml')
    os.remove(f'{UPLOADED_FILES_PATH}{str(config_from_db["name_config"])}.yaml')


async def test_failed_compile_endpoint_two(client, get_config_from_database):
    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp = resp.json()
    name_config = data_from_resp["name_config"]
    assert os.path.exists(f'{UPLOADED_FILES_PATH}{name_config}.yaml')

    fail_name_config = str(uuid4())
    resp = client.post("/compile", data=fail_name_config)
    config_from_db = await get_config_from_database(fail_name_config)
    data_from_resp = resp.json()

    assert resp.status_code == 404
    assert data_from_resp['message'] == 'Config not save'
    assert name_config != fail_name_config
    assert config_from_db == []
    assert resp.headers == [(b'content-length', b'29'), (b'content-type', b'application/json')]


async def test_failed_compile_endpoint(client, get_config_from_database):
    resp = client.post("/compile", data=None)
    config_from_db = await get_config_from_database(None)
    data_from_resp = resp.json()
    assert resp.status_code == 400
    assert data_from_resp['message'] == 'Config not save'
    assert config_from_db == []
    assert resp.headers == [(b'content-length', b'29'), (b'content-type', b'application/json')]


async def test_download_endpoint(client):
    resp = client.post("/download", data="dbe414e8-cca0-4f18-b041-7d0e44145794")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/octet-stream"

    expected_filename = "dbe414e8-cca0-4f18-b041-7d0e44145794.bin"
    assert resp.headers["Content-Disposition"] == f'attachment; filename="{expected_filename}"'

    with open(f"{COMPILE_DIR}dbe414e8-cca0-4f18-b041-7d0e44145794.bin", "rb") as file:
        file_content = file.read()
    assert resp.content == file_content


async def test_failed_download_endpoint(client):
    resp = client.post("/download", data=None)

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'
    assert resp.headers == [(b'content-length', b'48'), (b'content-type', b'application/json')]


async def test_failed_download_endpoint_two(client):
    resp = client.post("/download", data="")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'
    assert resp.headers == [(b'content-length', b'48'), (b'content-type', b'application/json')]


async def test_failed_download_endpoint_three(client):
    resp = client.post("/download", data="6be414e8-cca0-4f18-b041-7d0e44145794")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'
    assert resp.headers == [(b'content-length', b'48'), (b'content-type', b'application/json')]
