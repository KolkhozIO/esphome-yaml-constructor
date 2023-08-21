import json

from uuid import uuid4
from tests.conftest import create_test_token, decode_test_token
from tests.settings_tests import user_data, config_data, test_config_data, config_data_two, test_config_two_data


async def test_create_favourites(client, create_test_user, get_config_by_config_json, get_favourites_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Get favourites
    test_favourites_in_db = await get_favourites_from_database(data_from_resp['id'])
    assert len(test_favourites_in_db) == 1
    test_favourites_in_db = dict(test_favourites_in_db[0])

    # Get Config
    test_config_in_db = await get_config_by_config_json(json.dumps(config_data))
    assert len(test_config_in_db) == 1
    config_from_db = dict(test_config_in_db[0])

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp['name_config'] == str(config_from_db['name_config'])
    assert data_from_resp['name_esphome'] != config_from_db['name_esphome']
    assert data_from_resp['user_id'] == test_user['user_id']
    assert data_from_resp['user_id'] == test_favourites_in_db['user_id']
    assert data_from_resp['name_config'] == str(test_favourites_in_db['name_config'])
    assert data_from_resp['name_esphome'] == test_favourites_in_db['name_esphome']
    assert data_from_resp['id'] == test_favourites_in_db['id']


async def test_create_favourites_with_new_config(client, create_test_user, create_test_config, get_favourites_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    test_favourites_in_db = await get_favourites_from_database(data_from_resp['id'])
    assert len(test_favourites_in_db) == 1
    test_favourites_in_db = dict(test_favourites_in_db[0])

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp['name_config'] == str(config_from_db['name_config'])
    assert data_from_resp['name_esphome'] == config_from_db['name_esphome']
    assert data_from_resp['user_id'] == test_user['user_id']
    assert data_from_resp['user_id'] == test_favourites_in_db['user_id']
    assert data_from_resp['name_config'] == str(test_favourites_in_db['name_config'])
    assert data_from_resp['name_esphome'] == test_favourites_in_db['name_esphome']
    assert data_from_resp['id'] == test_favourites_in_db['id']


async def test_create_favourites_two(client, create_test_user, create_test_config, get_favourites_from_database, get_config_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**{
        'name_config': uuid4(),
        'hash_yaml': '205d5758d4cc066603a617faf6ad7c29',
        'name_esphome': 'edfhgkd',
        'platform': 'ESP32',
        'compile_test': False,
        'config_json': json.dumps(None)
    }))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    test_favourites_in_db = await get_favourites_from_database(data_from_resp['id'])
    assert len(test_favourites_in_db) == 1
    test_favourites_in_db = dict(test_favourites_in_db[0])

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp['name_config'] == str(config_from_db['name_config'])
    assert data_from_resp['name_esphome'] == config_from_db['name_esphome']
    assert data_from_resp['user_id'] == test_user['user_id']
    assert data_from_resp['user_id'] == test_favourites_in_db['user_id']
    assert data_from_resp['name_config'] == str(test_favourites_in_db['name_config'])
    assert data_from_resp['name_esphome'] == test_favourites_in_db['name_esphome']
    assert data_from_resp['id'] == test_favourites_in_db['id']

    config_db = await get_config_from_database(data_from_resp['name_config'])
    assert len(config_db) == 1
    config_db = dict(config_db[0])

    assert config_db['name_config'] == config_from_db['name_config']
    assert config_db['hash_yaml'] == config_from_db['hash_yaml']
    assert config_db['compile_test'] == config_from_db['compile_test']
    assert config_db['name_esphome'] == config_from_db['name_esphome']
    assert config_db['platform'] == config_from_db['platform']
    assert config_db['config_json'] != config_from_db['config_json']


async def test_create_favourites_three(client, create_test_user, get_favourites_from_database_by_user_id):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_one = resp.json()

    assert resp.status_code == 200
    test_favourites_in_db = await get_favourites_from_database_by_user_id(data_from_resp_one['user_id'])
    assert len(test_favourites_in_db) == 1

    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_two = resp.json()

    assert resp.status_code == 200
    test_favourites_in_db = await get_favourites_from_database_by_user_id(data_from_resp_two['user_id'])
    assert len(test_favourites_in_db) == 1

    resp = client.post(
        "/favourites",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_three = resp.json()

    assert resp.status_code == 200
    test_favourites_in_db = await get_favourites_from_database_by_user_id(data_from_resp_three['user_id'])
    assert len(test_favourites_in_db) == 2


async def test_create_favourites_fail(client, create_test_user, get_config_by_config_json, get_favourites_from_database_by_user_id):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {None}"}
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]

    config_db = await get_config_by_config_json(json.dumps(config_data))
    assert len(config_db) == 0

    favoutites_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(favoutites_db) == 0


async def test_create_favourites_fail_two(client, create_test_user, get_config_by_config_json, get_favourites_from_database_by_user_id):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data)
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Not authenticated"}'
    assert resp.headers == [(b'www-authenticate', b'Bearer'), (b'content-length', b'30'), (b'content-type', b'application/json')]

    config_db = await get_config_by_config_json(json.dumps(config_data))
    assert len(config_db) == 0

    favoutites_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(favoutites_db) == 0


async def test_create_favourites_fail_three(client, create_test_user, get_config_by_config_json, get_favourites_from_database_by_user_id):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(None),
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration was not sent"}'
    assert resp.headers == [(b'content-length', b'40'), (b'content-type', b'application/json')]

    config_db = await get_config_by_config_json(json.dumps(config_data))
    assert len(config_db) == 0

    favoutites_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(favoutites_db) == 0


async def test_create_favourites_fail_four(client, create_test_user, get_config_by_config_json, get_favourites_from_database_by_user_id):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps({}),
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert resp.status_code == 404
    assert resp.content == b'{"message":"esphhome name item not filled"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]

    config_db = await get_config_by_config_json(json.dumps(config_data))
    assert len(config_db) == 0

    favoutites_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(favoutites_db) == 0


async def test_create_favourites_fail_four(client, create_test_user, get_config_by_config_json, get_favourites_from_database_by_user_id):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(None),
        headers={"Authorization": f"Bearer {None}"}
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]

    config_db = await get_config_by_config_json(json.dumps(config_data))
    assert len(config_db) == 0

    favoutites_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(favoutites_db) == 0


async def test_delete_favourites(client, create_test_user, get_user_from_database_by_user_id, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database, get_config_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    test_favourites = dict((await create_favourites_in_database(
        id=1,
        user_id=test_user['user_id'],
        name_config=config_from_db['name_config'],
        name_esphome=config_from_db['name_esphome']
    ))[0])

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config={config_from_db['name_config']}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 0

    test_user = await get_user_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_user) == 1

    create_config_in_db = await get_config_from_database(test_favourites['name_config'])
    assert len(create_config_in_db) == 1

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp == 'favourites deleted'


async def test_delete_favourites_two(client, create_test_user, create_test_config, create_favourites_in_database, get_favourites_from_database_by_user_id, get_user_from_database_by_user_id, get_config_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    test_favourites = dict((await create_favourites_in_database(
        id=2,
        user_id=test_user['user_id'],
        name_config=config_from_db['name_config'],
        name_esphome=config_from_db['name_esphome']
    ))[0])

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config=dcf512d6-7829-4769-a5a3-ebd255c558ab",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    test_user = await get_user_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_user) == 1

    create_config_in_db = await get_config_from_database(test_favourites['name_config'])
    assert len(create_config_in_db) == 1

    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration with this name does not exist."}'
    assert resp.headers == [(b'content-length', b'58'), (b'content-type', b'application/json')]


async def test_delete_favourites_three(client, create_test_user, create_test_config, create_favourites_in_database, get_favourites_from_database_by_user_id, get_user_from_database_by_user_id, get_config_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    test_favourites = dict((await create_favourites_in_database(
        id=3,
        user_id=test_user['user_id'],
        name_config=config_from_db['name_config'],
        name_esphome=config_from_db['name_esphome']
    ))[0])

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config=None",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    test_user = await get_user_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_user) == 1

    create_config_in_db = await get_config_from_database(test_favourites['name_config'])
    assert len(create_config_in_db) == 1

    # Verify the response
    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'
    assert resp.headers == [(b'content-length', b'103'), (b'content-type', b'application/json')]


async def test_delete_favourites_four(client, create_test_user, create_test_config, create_favourites_in_database, get_favourites_from_database_by_user_id, get_user_from_database_by_user_id, get_config_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    test_favourites = dict((await create_favourites_in_database(
        id=4,
        user_id=test_user['user_id'],
        name_config=config_from_db['name_config'],
        name_esphome=config_from_db['name_esphome']
    ))[0])

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config={config_from_db['name_config']}",
        headers={"Authorization": f"Bearer {None}"}
    )

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    test_user = await get_user_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_user) == 1

    create_config_in_db = await get_config_from_database(test_favourites['name_config'])
    assert len(create_config_in_db) == 1

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]


async def test_delete_favourites_five(client, create_test_user, create_test_config, create_favourites_in_database, get_favourites_from_database_by_user_id, get_user_from_database_by_user_id, get_config_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    test_favourites = dict((await create_favourites_in_database(
        id=5,
        user_id=test_user['user_id'],
        name_config=config_from_db['name_config'],
        name_esphome=config_from_db['name_esphome']
    ))[0])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config=None",
        headers={"Authorization": f"Bearer {None}"}
    )

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_favourites_in_db) == 1

    test_user = await get_user_from_database_by_user_id(test_favourites['user_id'])
    assert len(test_user) == 1

    create_config_in_db = await get_config_from_database(test_favourites['name_config'])
    assert len(create_config_in_db) == 1

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]


async def test_get_all_favourites(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])
    config_two_from_db = dict((await create_test_config(**test_config_two_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=6,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    await create_favourites_in_database(id=7,
                                        user_id=test_user['user_id'],
                                        name_config=config_two_from_db['name_config'],
                                        name_esphome=config_two_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 2
    test_one_favourites_in_db = dict(test_favourites_in_db[0])
    test_two_favourites_in_db = dict(test_favourites_in_db[1])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/all",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    assert resp.status_code == 200
    assert str(test_one_favourites_in_db['name_config']) == (dict(data_from_resp[0]))['name_config']
    assert test_one_favourites_in_db['name_esphome'] == (dict(data_from_resp[0]))['name_esphome']
    assert str(test_two_favourites_in_db['name_config']) == (dict(data_from_resp[1]))['name_config']
    assert test_two_favourites_in_db['name_esphome'] == (dict(data_from_resp[1]))['name_esphome']
    assert str(config_from_db['name_config']) == (dict(data_from_resp[0]))['name_config']
    assert config_from_db['name_esphome'] == (dict(data_from_resp[0]))['name_esphome']
    assert str(config_two_from_db['name_config']) == (dict(data_from_resp[1]))['name_config']
    assert config_two_from_db['name_esphome'] == (dict(data_from_resp[1]))['name_esphome']


async def test_failed_get_all_favourites(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database, get_user_from_database_by_user_id, get_config_from_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])
    config_two_from_db = dict((await create_test_config(**test_config_two_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=8,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    await create_favourites_in_database(id=9,
                                        user_id=test_user['user_id'],
                                        name_config=config_two_from_db['name_config'],
                                        name_esphome=config_two_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 2
    test_one_favourites_in_db = dict(test_favourites_in_db[0])
    test_two_favourites_in_db = dict(test_favourites_in_db[1])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/all",
        headers={"Authorization": f"Bearer {None}"}
    )

    assert test_one_favourites_in_db['user_id'] == test_two_favourites_in_db['user_id']

    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_one_favourites_in_db['user_id'])
    assert len(test_favourites_in_db) == 2

    test_user = await get_user_from_database_by_user_id(test_one_favourites_in_db['user_id'])
    assert len(test_user) == 1

    create_config_in_db = await get_config_from_database(test_one_favourites_in_db['name_config'])
    assert len(create_config_in_db) == 1

    create_config_in_db = await get_config_from_database(test_two_favourites_in_db['name_config'])
    assert len(create_config_in_db) == 1

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]


async def test_get_one_favourites(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=10,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={config_from_db['name_config']}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 201
    assert json.loads(config_from_db['config_json']) == data_from_resp['json_text']
    assert config_data == data_from_resp['json_text']


async def test_get_one_favourites_two(client, create_test_user, create_test_config):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={config_from_db['name_config']}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 404
    assert json.loads(resp.text) == json.loads('{"message": "Favorites with the name of the ' +
                                               str(config_from_db["name_config"]) + ' are not found."}')
    assert resp.headers == [(b'content-length', b'96'), (b'content-type', b'application/json')]


async def test_get_one_favourites_three(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=11,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config=None",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Verify the response
    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'
    assert resp.headers == [(b'content-length', b'103'), (b'content-type', b'application/json')]


async def test_get_one_favourites_four(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=12,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={config_from_db['name_config']}",
        headers={"Authorization": f"Bearer {None}"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]


async def test_get_one_favourites_five(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=13,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={config_from_db['name_config']}",
        headers={"Authorization": f"Bearer vyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                  f".eyJzdWIiOiJ0cm9sb2xvMTIwMTIwQGdtYWlsLmNvbSIsImV4cCI6MTY5MTU3MTc4MX0"
                                  f".O7Fd_xP4hlxF0IrY483NlFotlqbyUxjZJJzoE698Fk8"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]


async def test_get_edit_favourites(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database, get_config_by_config_json):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=14,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1
    test_favourites_in_db = dict(test_favourites_in_db[0])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={config_from_db['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 200
    # Favorites changed
    assert test_favourites_in_db['user_id'] == data_from_resp['user_id']
    assert str(test_favourites_in_db['name_config']) != data_from_resp['name_config']
    assert test_favourites_in_db['name_esphome'] != data_from_resp['name_esphome']
    assert test_favourites_in_db['id'] != data_from_resp['id']
    # Checking if there are 2 different configs in the database
    check_config_one = await get_config_by_config_json(json.dumps(config_data))
    assert len(check_config_one) == 1
    check_config_one = dict(check_config_one[0])
    assert config_data_two != json.loads(check_config_one['config_json'])
    assert config_data == json.loads(check_config_one['config_json'])

    check_config_two = await get_config_by_config_json(json.dumps(config_data_two))
    assert len(check_config_two) == 1
    check_config_two = dict(check_config_two[0])
    assert config_data_two == json.loads(check_config_two['config_json'])
    assert config_data != json.loads(check_config_two['config_json'])


async def test_get_edit_favourites_two(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database, get_config_by_config_json):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])
    config_two_from_db = dict((await create_test_config(**test_config_two_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=15,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    await create_favourites_in_database(id=16,
                                        user_id=test_user['user_id'],
                                        name_config=config_two_from_db['name_config'],
                                        name_esphome=config_two_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 2
    test_one_favourites_in_db = dict(test_favourites_in_db[0])
    test_two_favourites_in_db = dict(test_favourites_in_db[1])

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={config_from_db['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 200
    # Favorites changed
    assert test_one_favourites_in_db['user_id'] == data_from_resp['user_id']
    assert str(test_one_favourites_in_db['name_config']) != data_from_resp['name_config']
    assert test_one_favourites_in_db['name_esphome'] != data_from_resp['name_esphome']
    assert test_one_favourites_in_db['id'] != data_from_resp['id']
    assert test_two_favourites_in_db['user_id'] == data_from_resp['user_id']
    assert str(test_two_favourites_in_db['name_config']) == data_from_resp['name_config']
    assert test_two_favourites_in_db['name_esphome'] == data_from_resp['name_esphome']
    assert test_two_favourites_in_db['id'] == data_from_resp['id']

    # Checking if the favorite was deleted, which was replaced by the same as the second one
    check_all_config = await get_favourites_from_database_by_user_id(data_from_resp['user_id'])
    assert len(check_all_config) == 1

    # Checking if there are 2 different configs in the database
    check_config_one = await get_config_by_config_json(json.dumps(config_data))
    assert len(check_config_one) == 1
    check_config_one = dict(check_config_one[0])
    assert config_data_two != json.loads(check_config_one['config_json'])
    assert config_data == json.loads(check_config_one['config_json'])

    check_config_two = await get_config_by_config_json(json.dumps(config_data_two))
    assert len(check_config_two) == 1
    check_config_two = dict(check_config_two[0])
    assert config_data_two == json.loads(check_config_two['config_json'])
    assert config_data != json.loads(check_config_two['config_json'])


async def test_get_edit_favourites_three(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database, get_config_by_config_json):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=17,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={config_from_db['name_config']}",
        data=json.dumps(None),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration was not sent"}'
    assert resp.headers == [(b'content-length', b'40'), (b'content-type', b'application/json')]
    # Checking if there are 2 different configs in the database
    check_config_one = await get_config_by_config_json(json.dumps(config_data))
    assert len(check_config_one) == 1
    check_config_one = dict(check_config_one[0])
    assert config_data_two != check_config_one['config_json']


async def test_get_edit_favourites_four(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database, get_config_by_config_json):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=18,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={config_from_db['name_config']}",
        data=json.dumps({}),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"esphhome name item not filled"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]
    # Checking if there are 2 different configs in the database
    check_config_one = await get_config_by_config_json(json.dumps(config_data))
    assert len(check_config_one) == 1
    check_config_one = dict(check_config_one[0])
    assert config_data_two != check_config_one['config_json']


async def test_get_edit_favourites_five(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database, get_config_by_config_json):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=19,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config=None",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'
    assert resp.headers == [(b'content-length', b'103'), (b'content-type', b'application/json')]
    # Checking if there are 2 different configs in the database
    check_config_one = await get_config_by_config_json(json.dumps(config_data))
    assert len(check_config_one) == 1
    check_config_one = dict(check_config_one[0])
    assert config_data_two != check_config_one['config_json']


async def test_get_edit_favourites_six(client, create_test_user, create_test_config, get_favourites_from_database_by_user_id, create_favourites_in_database, get_config_by_config_json):
    # Create a test user
    test_user = dict((await create_test_user(**user_data))[0])

    # Create a test configuration
    config_from_db = dict((await create_test_config(**test_config_data))[0])

    # Create a test favourites
    await create_favourites_in_database(id=20,
                                        user_id=str(test_user['user_id']),
                                        name_config=config_from_db['name_config'],
                                        name_esphome=config_from_db['name_esphome'])
    test_favourites_in_db = await get_favourites_from_database_by_user_id(test_user['user_id'])
    assert len(test_favourites_in_db) == 1

    # Create test token
    access_token = await create_test_token(test_user['email'])
    email = await decode_test_token(access_token)
    assert test_user['email'] == email

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={config_from_db['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {None}"}
    )
    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
    assert resp.headers == [(b'content-length', b'43'), (b'content-type', b'application/json')]
    # Checking if there are 2 different configs in the database
    check_config_one = await get_config_by_config_json(json.dumps(config_data))
    assert len(check_config_one) == 1
    check_config_one = dict(check_config_one[0])
    assert config_data_two != check_config_one['config_json']

