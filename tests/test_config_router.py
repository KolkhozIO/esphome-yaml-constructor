import json
import os
import uuid
from uuid import uuid4

from settings import COMPILE_DIR, UPLOADED_FILES_PATH, COMPILE_DIR_OTA
from tests.conftest import get_file_name
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

    file_name = get_file_name(resp.text)
    content = (
            b"INFO Reading configuration ./uploaded_files/"
            + file_name.encode("utf-8")
            + b".yaml...\n\nINFO Configuration is valid!\n\nesphome:\n\n  name: "
            + config_data['esphome']['name'].encode("utf-8")
            + b"\n\n  build_path: .esphome/build/"
            + config_data['esphome']['name'].encode("utf-8")
            + b"\n\n  friendly_name: ''\n\n  platformio_options: {}\n\n  includes: []\n\n  libraries: []"
              b"\n\n  name_add_mac_suffix: false\n\n  min_version: 2023.3.2\n\nesp32:\n\n  board: "
            + config_data['esp32']['board'].encode("utf-8")
            + b"\n\n  framework:\n\n    version: 2.0.5\n\n    source: ~3.20005.0"
              b"\n\n    platform_version: platformio/espressif32 @ 5.2.0\n\n    type: "
            + config_data['esp32']['framework']['type'].encode("utf-8")
            + b"\n\n  variant: ESP32\n\napi:\n\n  password: "
            + config_data['api']['password'].encode("utf-8")
            + b"\n\n  port: 6053\n\n  reboot_timeout: 15min\n\ni2c:\n\n- scan: true\n\n  scl: "
            + str(config_data['i2c']['scl']).encode("utf-8")
            + b"\n\n  sda: "
            + str(config_data['i2c']['sda']).encode("utf-8")
            + b"\n\n  frequency: 50000.0\n\nlogger:\n\n  baud_rate: "
            + str(config_data['logger']['baud_rate']).encode("utf-8")
            + b"\n\n  level: DEBUG\n\n  tx_buffer_size: 512\n\n  deassert_rts_dtr: false\n\n  hardware_uart: UART0"
              b"\n\n  logs: {}\n\nota:\n\n  password: "
            + config_data['ota']['password'].encode("utf-8")
            + b"\n\n  safe_mode: true\n\n  port: 3232\n\n  reboot_timeout: 5min\n\n  num_attempts: 10\n\nwifi:"
              b"\n\n  ap:\n\n    password: "
            + config_data['wifi']['ap']['password'].encode("utf-8")
            + b"\n\n    ssid: "
            + config_data['wifi']['ap']['ssid'].encode("utf-8")
            + b"\n\n    ap_timeout: 1min\n\n  domain: .local\n\n  reboot_timeout: 15min\n\n  power_save_mode: LIGHT"
              b"\n\n  fast_connect: false\n\n  networks:\n\n  - ssid: "
            + config_data['wifi']['ssid'].encode("utf-8")
            + b"\n\n    password: "
            + config_data['wifi']['password'].encode("utf-8")
            + b"\n\n    priority: 0.0\n\n  use_address: "
            + config_data['esphome']['name'].encode("utf-8")
            + b".local\n\n\n\n"
    )

    assert resp.status_code == 200
    assert resp.content == content


async def test_validate_endpoint_none_data(client):
    resp = client.post("/validate", data=json.dumps(None))

    file_name = get_file_name(resp.text)
    content = (
            b"INFO Reading configuration ./uploaded_files/"
            + file_name.encode('utf-8')
            + b".yaml...\n\nFailed config\n\n\n\n'esphome' section missing from configuration. "
              b"Please make sure your configuration has an 'esphome:' line in it.\n\n\n\n"
    )

    assert resp.status_code == 200
    assert resp.content == content


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

    content = (b"INFO Reading configuration ./uploaded_files/"
               + name_config.encode('utf-8')
               + b".yaml...\n\nFailed config\n\n\n\nwifi: [source ./uploaded_files/"
               + name_config.encode('utf-8')
               + b".yaml:18]\n\n  ap: \n\n    password: ''\n\n    \n\n    SSID can't be empty.\n\n    ssid: ''"
                 b"\n\n  password: ''\n\n  \n\n  SSID can't be empty.\n\n  ssid: ''\n\n")

    assert resp.status_code == 200
    assert resp.content == content
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

    assert resp.status_code == 400
    assert resp.json()['message'] == 'Config not save'


async def test_download_endpoint(client):
    resp = client.post("/download", data="dbe414e8-cca0-4f18-b041-7d0e44145794")
    assert resp.status_code == 200

    with open(f"{COMPILE_DIR}dbe414e8-cca0-4f18-b041-7d0e44145794.bin", "rb") as file:
        file_content = file.read()
    assert resp.content == file_content


async def test_failed_download_endpoint_none_data(client):
    resp = client.post("/download", data=None)

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_failed_download_endpoint_no_data(client):
    resp = client.post("/download", data="")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_failed_download_endpoint_fail_data(client):
    resp = client.post("/download", data="6be414e8-cca0-4f18-b041-7d0e44145794")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_download_ota_endpoint(client):
    resp = client.post("/download/ota", data="dbe414e8-cca0-4f18-b041-7d0e44145794")
    assert resp.status_code == 200

    with open(f"{COMPILE_DIR_OTA}dbe414e8-cca0-4f18-b041-7d0e44145794.bin", "rb") as file:
        file_content = file.read()
    assert resp.content == file_content


async def test_failed_download_ota_endpoint_none_data(client):
    resp = client.post("/download/ota", data=None)

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_failed_download_ota_endpoint_no_data(client):
    resp = client.post("/download/ota", data="")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'


async def test_failed_download_ota_endpoint_fail_data(client):
    resp = client.post("/download/ota", data="6be414e8-cca0-4f18-b041-7d0e44145794")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration was not compiled"}'

