import json
import os
import uuid

from tests.settings_tests import config_data, config_failed_data


async def create_share(client, config):
    resp = client.post("/share", data=json.dumps(config))
    data_from_resp = resp.json()

    assert resp.status_code == 201
    assert uuid.UUID(data_from_resp.get("uuid"), version=4) is not None

    url_front = os.environ.get('REACT_APP_APP_URL')
    name_config = data_from_resp["uuid"]
    url = f"{url_front}/config?uuid={name_config}"
    assert data_from_resp["url"] == url
    return name_config


async def test_share_config(client):
    name_config = await create_share(client, config_data)

    resp = client.get(f"/share/?file_name={name_config}")
    data_from_resp = resp.json()

    assert resp.status_code == 201
    assert data_from_resp["json_text"] == config_data


async def test_share_config_bad_config_data(client):
    name_config = await create_share(client, config_failed_data)

    resp = client.get(f"/share/?file_name={name_config}")
    data_from_resp = resp.json()

    assert resp.status_code == 201
    assert data_from_resp["json_text"] == config_failed_data


async def test_share_config_fail_data_none(client):
    resp = client.post("/share", data=json.dumps(None))

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration was not sent"}'


async def test_share_config_fail_bad_name_config(client):
    await create_share(client, config_data)

    fail_name_config = str(uuid.uuid4())
    resp = client.get(f"/share/?file_name={fail_name_config}")

    assert resp.status_code == 404
    assert resp.content == b'{"message":"The configuration you are trying to access does not exist with the same name."}'


async def test_share_config_fail_none_name_config(client):
    await create_share(client, config_data)

    resp = client.get(f"/share/?file_name=None")

    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","file_name"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'


async def test_share_config_fail_no_name_config(client):
    await create_share(client, config_data)

    resp = client.get(f"/share/?file_name=")

    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","file_name"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'
