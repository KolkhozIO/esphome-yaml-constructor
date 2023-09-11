import json
import uuid

from tests.settings_tests import config_data, config_data_two, google_profile_one


async def test_create_favourites(client):
    resp = client.post("/google/login", json=google_profile_one)
    access_token = resp.json()['access_token']

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp.get("name_config"), version=4) is not None
    assert data_from_resp['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp['id'], int)


async def test_create_favourites_with_new_config(client):
    resp = client.post("/google/login", json=google_profile_one)
    access_token = resp.json()['access_token']

    # Create a test configuration
    resp = client.post("/share", data=json.dumps(config_data))
    data_from_resp_share = resp.json()

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_two = resp.json()

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp_two['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_two.get("name_config"), version=4) is not None
    assert data_from_resp_two['name_config'] == data_from_resp_share['uuid']
    assert data_from_resp_two['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_two['id'], int)


async def test_create_favourites_with_new_config_two(client):
    resp = client.post("/google/login", json=google_profile_one)
    access_token = resp.json()['access_token']

    # Create a test configuration
    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp_one = resp.json()

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_two = resp.json()

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp_two['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_two.get("name_config"), version=4) is not None
    assert data_from_resp_two['name_config'] == data_from_resp_one['name_config']
    assert data_from_resp_two['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_two['id'], int)


async def test_create_favourites_with_new_config_three(client):
    resp = client.post("/google/login", json=google_profile_one)
    access_token = resp.json()['access_token']

    # Create a test configuration
    resp = client.post("/share", data=json.dumps(config_data))
    data_from_resp_share = resp.json()

    resp = client.post("/save_config", data=json.dumps(config_data))
    data_from_resp_one = resp.json()

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_two = resp.json()

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp_two['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_two.get("name_config"), version=4) is not None
    assert data_from_resp_two['name_config'] == data_from_resp_share['uuid']
    assert data_from_resp_two['name_config'] == data_from_resp_one['name_config']
    assert data_from_resp_two['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_two['id'], int)


async def test_create_favourites_three(client):
    resp = client.post("/google/login", json=google_profile_one)
    access_token = resp.json()['access_token']

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_one = resp.json()
    assert resp.status_code == 200
    assert data_from_resp_one['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_one.get("name_config"), version=4) is not None
    assert data_from_resp_one['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_one['id'], int)

    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_two = resp.json()
    assert resp.status_code == 200
    assert data_from_resp_two['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_two.get("name_config"), version=4) is not None
    assert data_from_resp_two['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_two['id'], int)

    resp = client.post(
        "/favourites",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_three = resp.json()
    assert resp.status_code == 200
    assert data_from_resp_three['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_three.get("name_config"), version=4) is not None
    assert data_from_resp_three['name_esphome'] == config_data_two['esphome']['name']
    assert isinstance(data_from_resp_three['id'], int)

    assert data_from_resp_one['id'] == data_from_resp_two['id']
    assert data_from_resp_one['name_config'] == data_from_resp_two['name_config']

    assert data_from_resp_one['id'] != data_from_resp_three['id']
    assert data_from_resp_one['user_id'] == data_from_resp_three['user_id']
    assert data_from_resp_one['name_config'] != data_from_resp_three['name_config']
    assert data_from_resp_one['name_esphome'] != data_from_resp_three['name_esphome']


async def test_create_favourites_fail(client):
    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {None}"}
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_create_favourites_fail_two(client):
    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data)
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Not authenticated"}'


async def test_create_favourites_fail_three(client):
    resp = client.post("/google/login", json=google_profile_one)
    access_token = resp.json()['access_token']

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(None),
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration was not sent"}'


async def test_create_favourites_fail_four(client):
    resp = client.post("/google/login", json=google_profile_one)
    access_token = resp.json()['access_token']

    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps({}),
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert resp.status_code == 404
    assert resp.content == b'{"message":"esphhome name item not filled"}'


async def test_create_favourites_fail_four(client):
    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(None),
        headers={"Authorization": f"Bearer {None}"}
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_delete_favourites(client):
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test configuration
    resp = client.post("/save_config", data=json.dumps(config_data))
    assert resp.status_code == 200

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_from_resp_favourites = resp.json()

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config={data_from_resp_favourites['name_config']}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_del = resp.json()

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp_del == 'favourites deleted'


async def test_delete_favourites_two(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test configuration
    resp = client.post("/save_config", data=json.dumps(config_data))
    assert resp.status_code == 200

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config=dcf512d6-7829-4769-a5a3-ebd255c558ab",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration with this name does not exist."}'


async def test_delete_favourites_three(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config=None",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Verify the response
    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'


async def test_delete_favourites_four(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test configuration
    resp = client.post("/save_config", data=json.dumps(config_data))
    assert resp.status_code == 200

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_from_resp_favourites = resp.json()

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config={data_from_resp_favourites['name_config']}",
        headers={"Authorization": f"Bearer {None}"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_delete_favourites_five(client):
    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config=None",
        headers={"Authorization": f"Bearer {None}"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_get_all_favourites(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    resp = client.post(
        "/favourites",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_two = resp.json()

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/all",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_favourites_all = resp.json()

    assert resp.status_code == 200
    assert str(data_favourites_one['name_config']) == (dict(data_favourites_all[0]))['name_config']
    assert data_favourites_one['name_esphome'] == (dict(data_favourites_all[0]))['name_esphome']
    assert str(data_favourites_two['name_config']) == (dict(data_favourites_all[1]))['name_config']
    assert data_favourites_two['name_esphome'] == (dict(data_favourites_all[1]))['name_esphome']


async def test_failed_get_all_favourites(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200

    resp = client.post(
        "/favourites",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/all",
        headers={"Authorization": f"Bearer {None}"}
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_get_one_favourites(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={data_favourites_one['name_config']}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 201
    assert config_data == data_from_resp['json_text']


async def test_get_one_favourites_two(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test configuration
    resp = client.post("/save_config", data=json.dumps(config_data))
    assert resp.status_code == 200
    data_config_one = resp.json()

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={data_config_one['name_config']}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 404
    assert json.loads(resp.text) == json.loads('{"message": "Favorites with the name of the ' +
                                               str(data_config_one["name_config"]) + ' are not found."}')


async def test_get_one_favourites_three(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config=None",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Verify the response
    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'


async def test_get_one_favourites_four(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={data_favourites_one['name_config']}",
        headers={"Authorization": f"Bearer {None}"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_get_one_favourites_five(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={data_favourites_one['name_config']}",
        headers={"Authorization": f"Bearer vyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                  f".eyJzdWIiOiJ0cm9sb2xvMTIwMTIwQGdtYWlsLmNvbSIsImV4cCI6MTY5MTU3MTc4MX0"
                                  f".O7Fd_xP4hlxF0IrY483NlFotlqbyUxjZJJzoE698Fk8"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_get_edit_favourites(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_favourites_one['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 200
    # Favorites changed
    assert data_favourites_one['user_id'] == data_from_resp['user_id']
    assert str(data_favourites_one['name_config']) != data_from_resp['name_config']
    assert data_favourites_one['name_esphome'] != data_from_resp['name_esphome']
    assert data_favourites_one['id'] != data_from_resp['id']


async def test_get_edit_favourites_two(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    resp = client.post(
        "/favourites",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_two = resp.json()

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_favourites_one['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 200
    # Favorites changed
    assert data_favourites_one['user_id'] == data_from_resp['user_id']
    assert str(data_favourites_one['name_config']) != data_from_resp['name_config']
    assert data_favourites_one['name_esphome'] != data_from_resp['name_esphome']
    assert data_favourites_one['id'] != data_from_resp['id']

    assert data_favourites_two['user_id'] == data_from_resp['user_id']
    assert str(data_favourites_two['name_config']) == data_from_resp['name_config']
    assert data_favourites_two['name_esphome'] == data_from_resp['name_esphome']
    assert data_favourites_two['id'] == data_from_resp['id']


async def test_get_edit_favourites_three(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_favourites_one['name_config']}",
        data=json.dumps(None),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration was not sent"}'


async def test_get_edit_favourites_four(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_favourites_one['name_config']}",
        data=json.dumps({}),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"esphhome name item not filled"}'


async def test_get_edit_favourites_five(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config=None",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid","type":"type_error.uuid"}]}'


async def test_get_edit_favourites_six(client):
    # Create test token
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    # Create a test favourites
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data_favourites_one = resp.json()

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_favourites_one['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {None}"}
    )
    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'

