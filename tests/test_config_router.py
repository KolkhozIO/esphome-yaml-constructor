import json
import os
import uuid
from uuid import uuid4

from settings import COMPILE_DIR, UPLOADED_FILES_PATH, COMPILE_DIR_OTA
from tests.settings_tests import config_data, config_failed_data


async def create_config(client, config):
    resp = client.post("/save_config", data=json.dumps(config))
    data_from_resp_config = resp.json()

    assert resp.status_code == 200
    assert uuid.UUID(data_from_resp_config.get("name_config"), version=4) is not None
    os.remove(f'{UPLOADED_FILES_PATH}{data_from_resp_config.get("name_config")}.yaml')
    return data_from_resp_config["name_config"]


async def test_validate_endpoint(client):
    resp = client.post("/validate", data=json.dumps(config_data))

    assert resp.status_code == 200

    expected_strings = [
        config_data['esphome']['name'],
        config_data['esp32']['board'],
        config_data['esp32']['framework']['type'],
        config_data['api']['password'],
        str(config_data['i2c']['scl']),
        str(config_data['i2c']['sda']),
        str(config_data['logger']['baud_rate']),
        config_data['ota']['password'],
        config_data['wifi']['ap']['password'],
        config_data['wifi']['ap']['ssid'],
        config_data['wifi']['ssid'],
        config_data['wifi']['password'],
        config_data['esphome']['name']
    ]

    for expected_string in expected_strings:
        assert expected_string.encode("utf-8") in resp.content
    assert "INFO Configuration is valid!" in resp.text


async def test_validate_endpoint_none_data(client):
    resp = client.post("/validate", data=json.dumps(None))

    assert resp.status_code == 200
    assert "Failed config" in resp.text


async def test_save_config(client):
    await create_config(client, config_data)


async def test_save_two_config(client):
    data_from_resp_config_one = await create_config(client, config_data)
    data_from_resp_config_two = await create_config(client, config_data)
    assert data_from_resp_config_one == data_from_resp_config_two


async def test_save_config_after_share(client):
    resp = client.post("/share", data=json.dumps(config_data))
    data_from_resp_one = resp.json()
    assert resp.status_code == 201
    assert uuid.UUID(data_from_resp_one["uuid"], version=4) is not None

    data_from_resp_config = await create_config(client, config_data)
    assert data_from_resp_one["uuid"] == data_from_resp_config


async def test_failed_save_config_none_data(client):
    resp = client.post("/save_config", data=json.dumps(None))

    assert resp.status_code == 404
    assert resp.json()['detail'] == 'Item not found'


async def test_compile_endpoint(client):
    resp = client.post("/save_config", data=json.dumps(config_data))
    name_config = resp.json()["name_config"]

    resp = client.post("/compile", data=name_config)

    assert resp.status_code == 200
    assert "INFO Successfully compiled program." in resp.text
    os.remove(f'{COMPILE_DIR}{name_config}.bin')
    os.remove(f'{COMPILE_DIR_OTA}{name_config}.bin')


async def test_compile_endpoint_with_failed_config(client):
    resp = client.post("/save_config", data=json.dumps(config_failed_data))
    name_config = resp.json()["name_config"]

    resp = client.post("/compile", data=name_config)

    assert resp.status_code == 200
    assert "Failed config" in resp.text
    os.remove(f'{UPLOADED_FILES_PATH}{name_config}.yaml')


async def test_failed_compile_endpoint_fail_name_config(client):
    resp = client.post("/save_config", data=json.dumps(config_data))
    name_config = resp.json()["name_config"]
    fail_name_config = str(uuid4())
    assert name_config != fail_name_config

    resp = client.post("/compile", data=fail_name_config)

    assert resp.status_code == 404
    assert resp.json()['message'] == 'Config not save'
    os.remove(f'{UPLOADED_FILES_PATH}{name_config}.yaml')


async def test_failed_compile_endpoint_none_data(client):
    resp = client.post("/compile", data=None)

    assert resp.status_code == 404
    assert resp.json()['message'] == 'Config not save'


async def test_download_endpoint(client):
    resp = client.post("/download", data="dbe414e8-cca0-4f18-b041-7d0e44145794")
    assert resp.status_code == 200
    assert "Content-Disposition" in resp.headers


async def test_failed_download_endpoint_none_data(client):
    resp = client.post("/download", data=None)
    assert "Content-Disposition" not in resp.headers

    assert resp.status_code == 404
    assert "Content-Disposition" not in resp.headers
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_failed_download_endpoint_no_data(client):
    resp = client.post("/download", data="")

    assert resp.status_code == 404
    assert "Content-Disposition" not in resp.headers
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_failed_download_endpoint_fail_data(client):
    resp = client.post("/download", data="6be414e8-cca0-4f18-b041-7d0e44145794")

    assert resp.status_code == 404
    assert "Content-Disposition" not in resp.headers
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_download_ota_endpoint(client):
    resp = client.post("/download/ota", data="dbe414e8-cca0-4f18-b041-7d0e44145794")
    assert resp.status_code == 200
    assert "Content-Disposition" in resp.headers


async def test_failed_download_ota_endpoint_none_data(client):
    resp = client.post("/download/ota", data=None)

    assert resp.status_code == 404
    assert "Content-Disposition" not in resp.headers
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_failed_download_ota_endpoint_no_data(client):
    resp = client.post("/download/ota", data="")

    assert resp.status_code == 404
    assert "Content-Disposition" not in resp.headers
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_failed_download_ota_endpoint_fail_data(client):
    resp = client.post("/download/ota", data="6be414e8-cca0-4f18-b041-7d0e44145794")

    assert resp.status_code == 404
    assert "Content-Disposition" not in resp.headers
    assert resp.content == b'{"message":"The configuration was not compiled"}'

