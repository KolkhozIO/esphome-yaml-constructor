import json
import os

from settings import COMPILE_DIR
from tests.settings_tests import config_data


async def test_flash_endpoint_get_manifest(client, create_config_in_database, get_config_from_database):
    manifest_data = {
      'name': 'KOLKHOZ CONFIG',
      'home_assistant_domain': 'esphome',
      'new_install_skip_erase': False,
      'builds': [
        {
          'chipFamily': 'ESP32',
          'parts': [
            {
              'path': '/manifest/bin/dbe414e8-cca0-4f18-b041-7d0e44145794.bin',
              'offset': 0
            }
          ]
        }
      ]
    }
    await create_config_in_database(name_config="dbe414e8-cca0-4f18-b041-7d0e44145794",
                                    hash_yaml="205d5758d4cc066603a617faf6ad7c29",
                                    compile_test=True,
                                    name_esphome="edfhgkd",
                                    platform="ESP32",
                                    config_json=json.dumps(config_data))

    resp = client.get("/manifest/dbe414e8-cca0-4f18-b041-7d0e44145794")
    data_from_resp = resp.json()
    config_from_db = await get_config_from_database("dbe414e8-cca0-4f18-b041-7d0e44145794")

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 200
    assert data_from_resp == manifest_data
    assert data_from_resp["builds"][0]["chipFamily"] == config_from_db["platform"]
    assert data_from_resp["builds"][0]["parts"][0]["path"] == "/manifest/bin/dbe414e8-cca0-4f18-b041-7d0e44145794.bin"
    assert resp.headers["Content-Type"] == "application/json"
    assert resp.headers["Content-Length"] == "211"


async def test_flash_endpoint_get_manifest_two(client, create_config_in_database, get_config_from_database):
    await create_config_in_database(name_config="dbe414e8-cca0-4f18-b041-7d0e44145794",
                                    hash_yaml="205d5758d4cc066603a617faf6ad7c29",
                                    compile_test=True,
                                    name_esphome="edfhgkd",
                                    platform="ESP32",
                                    config_json=json.dumps(config_data))

    resp = client.get("/manifest/2be414e8-cca0-4f18-b041-7d0e44145794")
    config_from_db = await get_config_from_database("dbe414e8-cca0-4f18-b041-7d0e44145794")
    config_failed_from_db = await get_config_from_database("2be414e8-cca0-4f18-b041-7d0e44145794")

    assert len(config_from_db) == 1
    assert len(config_failed_from_db) == 0
    assert resp.status_code == 404
    assert resp.content == b'{"message":"A configuration with that name has not yet been compiled."}'
    assert resp.headers == [(b'content-length', b'71'), (b'content-type', b'application/json')]


async def test_flash_endpoint_get_manifest_three(client):
    resp = client.get("/manifest/None")

    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["path","file_name"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'
    assert resp.headers == [(b'content-length', b'100'), (b'content-type', b'application/json')]


async def test_flash_endpoint_get_manifest_four(client):
    resp = client.get("/manifest/")

    assert resp.status_code == 404
    assert resp.content == b'{"detail":"Not Found"}'
    assert resp.headers == [(b'content-length', b'22'), (b'content-type', b'application/json')]


async def test_flash_endpoint_get_bin(client):
    filename = "dbe414e8-cca0-4f18-b041-7d0e44145794.bin"
    assert os.path.exists(f'{COMPILE_DIR}{filename}')

    resp = client.get(f"/manifest/bin/{filename}")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/octet-stream"
    assert resp.headers["Content-Length"] == "874400"

    with open(f"{COMPILE_DIR}{filename}", "rb") as file:
        file_content = file.read()
    assert resp.content == file_content


async def test_flash_endpoint_get_bin_two(client):
    filename = "dbe414e8-cca0-4f18-b041-7d0e44145794.bin"
    assert os.path.exists(f'{COMPILE_DIR}{filename}')

    filename = "2be414e8-cca0-4f18-b041-7d0e44145794.bin"
    assert not os.path.exists(f'{COMPILE_DIR}{filename}')

    resp = client.get(f"/manifest/bin/{filename}")
    assert resp.status_code == 404
    assert resp.content == b'{"message":"The manifest contains a path to a file that does not exist."}'
    assert resp.headers == [(b'content-length', b'73'), (b'content-type', b'application/json')]


async def test_flash_endpoint_get_bin_three(client):
    resp = client.get(f"/manifest/bin/None")

    assert resp.status_code == 404
    assert resp.content == b'{"detail":"Not Found"}'
    assert resp.headers == [(b'content-length', b'22'), (b'content-type', b'application/json')]


async def test_flash_endpoint_get_bin_four(client):
    resp = client.get(f"/manifest/bin/")

    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["path","file_name"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'
    assert resp.headers == [(b'content-length', b'100'), (b'content-type', b'application/json')]
