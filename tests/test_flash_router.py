import json
import os

from settings import COMPILE_DIR, UPLOADED_FILES_PATH
from tests.settings_tests import config_data


async def test_flash_endpoint_get_manifest(client):
    # Create a test configuration
    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp_one = resp.json()

    resp = client.get(f"/manifest/{data_from_resp_one['name_config']}")
    data_from_resp = resp.json()

    assert resp.status_code == 200
    assert data_from_resp == {
        'name': 'KOLKHOZ CONFIG',
        'home_assistant_domain': 'esphome',
        'new_install_skip_erase': False,
        'builds': [
            {
                'chipFamily': 'ESP32',
                'parts': [
                    {
                        'path': f'/manifest/bin/{data_from_resp_one["name_config"]}.bin',
                        'offset': 0
                    }
                ]
            }
        ]
    }
    os.remove(f'{UPLOADED_FILES_PATH}{data_from_resp_one["name_config"]}.yaml')


async def test_flash_endpoint_fail_bad_name_config(client):
    # Create a test configuration
    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp_one = resp.json()

    resp = client.get("/manifest/2be414e8-cca0-4f18-b041-7d0e44145794")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"A configuration with that name has not yet been compiled."}'
    os.remove(f'{UPLOADED_FILES_PATH}{data_from_resp_one["name_config"]}.yaml')


async def test_flash_endpoint_fail_none_name_config(client):
    resp = client.get("/manifest/None")

    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["path","file_name"],"msg":"value is not a valid uuid",' \
                           b'"type":"type_error.uuid"}]}'


async def test_flash_endpoint_fail_no_name_config(client):
    resp = client.get("/manifest/")

    assert resp.status_code == 404
    assert resp.content == b'{"detail":"Not Found"}'


async def test_flash_endpoint_get_bin(client):
    filename = "dbe414e8-cca0-4f18-b041-7d0e44145794.bin"

    resp = client.get(f"/manifest/bin/{filename}")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/octet-stream"
    assert len(resp.content) > 0


async def test_flash_endpoint_fail_no_existent_bin(client):
    filename = "2be414e8-cca0-4f18-b041-7d0e44145794.bin"

    resp = client.get(f"/manifest/bin/{filename}")
    assert resp.status_code == 404
    assert resp.content == b'{"message":"The manifest contains a path to a file that does not exist."}'


async def test_flash_endpoint_fail_none_filename_bin(client):
    resp = client.get(f"/manifest/bin/None")

    assert resp.status_code == 404
    assert resp.content == b'{"detail":"Not Found"}'


async def test_flash_endpoint_fail_no_filename_bin(client):
    resp = client.get(f"/manifest/bin/")

    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["path","file_name"],"msg":"value is not a valid uuid",' \
                           b'"type":"type_error.uuid"}]}'
