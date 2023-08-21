import json
import os
from uuid import UUID, uuid4

from tests.conftest import get_hash_config
from tests.settings_tests import config_data, config_failed_data


name_config = None


async def test_share_config(client, get_config_from_database):
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


async def test_share_config_three(client):
    resp = client.post("/share", data=json.dumps(None))

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration was not sent"}'
    assert resp.headers == [(b'content-length', b'40'), (b'content-type', b'application/json')]


async def test_share_config_five(client, get_config_from_database):
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
