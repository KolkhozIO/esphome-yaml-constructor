import hashlib
import json
import os
from uuid import UUID, uuid4

import yaml


name_config = None
config_data = {
        'esphome': {
            'name': 'edfhgkd'
        },
        'esp32': {
            'board': 'esp32doit-devkit-v1',
            'framework': {
                'type': 'arduino'
            }
        },
        'api': {
            'password': 'password'
        },
        'ota': {
            'password': 'password'
        },
        'wifi': {
            'password': 'password',
            'ap': {
                'password': 'password',
                'ssid': 'sdfg'
            },
            'ssid': '23dc'
        },
        'logger': {
            'level': 'debug',
            'baud_rate': 1024
        },
        'i2c': {
            'sda': 21,
            'scl': 22,
            'scan': True
        }
    }


config_failed_data = {
    'esphome': {
        'name': ''
    },
    'esp32': {
        'board': 'esp32doit-devkit-v1',
        'framework': {
            'type': 'arduino'
        }
    },
    'api': {
        'password': ''
    },
    'ota': {
        'password': ''
    },
    'wifi': {
        'password': '',
        'ap': {
            'password': '',
            'ssid': ''
        },
        'ssid': ''
    },
    'logger': {
        'level': 'debug'
    },
    'i2c': {
        'sda': 21,
        'scl': 22,
        'scan': True
    }
}


def get_hash_config(config_data):
    yaml_text = yaml.dump(config_data)
    m = hashlib.md5()
    m.update(yaml_text.encode('utf-8'))
    return m.hexdigest()


def get_file_name(data_from_resp):
    start_text = "./uploaded_files/"
    end_text = ".yaml"

    start_index = data_from_resp.find(start_text) + len(start_text)
    end_index = data_from_resp.find(end_text, start_index)

    extracted_content = data_from_resp[start_index:end_index]
    return extracted_content


async def test_share_config(client, get_config_from_database):
    global name_config
    global config_data

    resp = client.post("/share", data=json.dumps(config_data))
    data_from_resp = resp.json()
    config_from_db = await get_config_from_database(data_from_resp["uuid"])

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 201
    assert config_from_db["name_config"] is not None
    assert config_from_db["name_config"] == UUID(data_from_resp["uuid"])
    assert config_from_db["hash_yaml"] is not None
    assert config_from_db["hash_yaml"] == get_hash_config(config_data)
    assert json.loads(config_from_db["config_json"]) == config_data

    url_front = os.environ.get('REACT_APP_APP_URL')
    name_config = config_from_db["name_config"]
    url = f"{url_front}/config?uuid={name_config}"
    assert data_from_resp["url"] == url

    resp = client.get(f"/share/?file_name={name_config}")
    data_from_resp = resp.json()

    assert resp.status_code == 201
    assert data_from_resp["json_text"] == config_data


async def test_share_config_two(client, get_config_from_database):
    resp = client.post("/share", data=json.dumps(config_failed_data))
    data_from_resp = resp.json()
    config_from_db = await get_config_from_database(data_from_resp["uuid"])

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 201
    assert config_from_db["name_config"] is not None
    assert config_from_db["name_config"] == UUID(data_from_resp["uuid"])
    assert config_from_db["hash_yaml"] is not None
    assert config_from_db["hash_yaml"] == get_hash_config(config_failed_data)
    assert json.loads(config_from_db["config_json"]) == config_failed_data

    url_front = os.environ.get('REACT_APP_APP_URL')
    name_config = config_from_db["name_config"]
    url = f"{url_front}/config?uuid={name_config}"
    assert data_from_resp["url"] == url

    resp = client.get(f"/share/?file_name={name_config}")
    data_from_resp = resp.json()

    assert resp.status_code == 201
    assert data_from_resp["json_text"] == config_failed_data


async def test_share_config_three(client, get_config_from_database):
    resp = client.post("/share", data=json.dumps(None))

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration was not sent"}'
    assert resp.headers == [(b'content-length', b'40'), (b'content-type', b'application/json')]


async def test_share_config_four(client, get_config_from_database):
    resp = client.post("/share", data=json.dumps({}))

    assert resp.status_code == 404
    assert resp.content == b'{"message":"esphhome name item not filled"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]


async def test_share_config_five(client, get_config_from_database):
    global name_config
    global config_data

    resp = client.post("/share", data=json.dumps(config_data))
    data_from_resp = resp.json()
    config_from_db = await get_config_from_database(data_from_resp["uuid"])

    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 201
    assert config_from_db["name_config"] is not None
    assert config_from_db["name_config"] == UUID(data_from_resp["uuid"])
    assert config_from_db["hash_yaml"] is not None
    assert config_from_db["hash_yaml"] == get_hash_config(config_data)
    assert json.loads(config_from_db["config_json"]) == config_data

    url_front = os.environ.get('REACT_APP_APP_URL')
    name_config = config_from_db["name_config"]
    url = f"{url_front}/config?uuid={name_config}"
    assert data_from_resp["url"] == url

    fail_name_config = str(uuid4())
    resp = client.get(f"/share/?file_name={fail_name_config}")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration you are trying to access does not exist with the same name."}'
    assert resp.headers == [(b'content-length', b'91'), (b'content-type', b'application/json')]
