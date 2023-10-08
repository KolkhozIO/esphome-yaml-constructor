import json
import os
import uuid

from settings import UPLOADED_FILES_PATH
from tests.settings_tests import config_data, config_data_two, google_profile_one


async def authenticate_and_create_favourites(client, google_profile, *configs):
    resp = client.post("/google/login", json=google_profile)
    assert resp.status_code == 200
    access_token = resp.json()['access_token']

    data_from_resp_favourites_list = []

    for config in configs:
        # Send the request with authentication token
        resp = client.post(
            "/favourites",
            data=json.dumps(config),
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert resp.status_code == 200
        data_from_resp_favourites = resp.json()
        data_from_resp_favourites_list.append(data_from_resp_favourites)

    return access_token, data_from_resp_favourites_list


async def test_create_favourites(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]
    # Verify the response
    assert data_from_resp_favourites['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_favourites.get("name_config"), version=4) is not None
    assert data_from_resp_favourites['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_favourites['id'], int)


async def test_create_favorites_with_an_existing_config_using_share(client):
    # Create a test configuration
    resp = client.post("/share", data=json.dumps(config_data))
    assert resp.status_code == 201
    data_from_resp_share = resp.json()

    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]
    # Verify the response
    assert data_from_resp_favourites['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_favourites.get("name_config"), version=4) is not None
    assert data_from_resp_favourites['name_config'] == data_from_resp_share['uuid']
    assert data_from_resp_favourites['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_favourites['id'], int)


async def test_create_favorites_with_an_existing_config_using_save(client):
    # Create a test configuration
    resp = client.post("/save_config", data=json.dumps(config_data))
    assert resp.status_code == 200
    data_from_resp_save = resp.json()

    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Verify the response
    assert data_from_resp_favourites['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_favourites.get("name_config"), version=4) is not None
    assert data_from_resp_favourites['name_config'] == data_from_resp_save['name_config']
    assert data_from_resp_favourites['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_favourites['id'], int)
    os.remove(f'{UPLOADED_FILES_PATH}{data_from_resp_save["name_config"]}.yaml')


async def test_create_favorites_with_an_existing_config_using_share_and_save(client):
    # Create a test configuration
    resp = client.post("/share", data=json.dumps(config_data))
    assert resp.status_code == 201
    data_from_resp_share = resp.json()

    resp = client.post("/save_config", data=json.dumps(config_data))
    assert resp.status_code == 200
    data_from_resp_save = resp.json()

    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Verify the response
    assert data_from_resp_favourites['user_id'] == google_profile_one['googleId']
    assert uuid.UUID(data_from_resp_favourites.get("name_config"), version=4) is not None
    assert data_from_resp_favourites['name_config'] == data_from_resp_share['uuid']
    assert data_from_resp_favourites['name_config'] == data_from_resp_save['name_config']
    assert data_from_resp_favourites['name_esphome'] == config_data['esphome']['name']
    assert isinstance(data_from_resp_favourites['id'], int)
    os.remove(f'{UPLOADED_FILES_PATH}{data_from_resp_save["name_config"]}.yaml')


async def creating_favorites_two_identical_and_one_different(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data, config_data,
                                                                                            config_data_two)
    data_from_resp_favourites = data_from_resp_favourites_list[0]
    data_from_resp_favourites_two = data_from_resp_favourites_list[1]
    data_from_resp_favourites_three = data_from_resp_favourites_list[2]

    assert data_from_resp_favourites['id'] == data_from_resp_favourites_two['id']
    assert data_from_resp_favourites['name_config'] == data_from_resp_favourites_two['name_config']

    assert data_from_resp_favourites['id'] != data_from_resp_favourites_three['id']
    assert data_from_resp_favourites['user_id'] == data_from_resp_favourites_three['user_id']
    assert data_from_resp_favourites['name_config'] != data_from_resp_favourites_three['name_config']
    assert data_from_resp_favourites['name_esphome'] != data_from_resp_favourites_three['name_esphome']

    assert data_from_resp_favourites_two['id'] != data_from_resp_favourites_three['id']
    assert data_from_resp_favourites_two['user_id'] == data_from_resp_favourites_three['user_id']
    assert data_from_resp_favourites_two['name_config'] != data_from_resp_favourites_three['name_config']
    assert data_from_resp_favourites_two['name_esphome'] != data_from_resp_favourites_three['name_esphome']


async def test_create_favourites_fail_no_token(client):
    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data),
        headers={"Authorization": f"Bearer {None}"}
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_create_favourites_fail_no_headers_auth(client):
    # Send the request with authentication token
    resp = client.post(
        "/favourites",
        data=json.dumps(config_data)
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Not authenticated"}'


async def test_create_favourites_fail_no_config(client):
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


async def test_create_favourites_fail_item_not_filled(client):
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


async def test_create_favourites_fail_no_config_and_token(client):
    resp = client.post(
        "/favourites",
        data=json.dumps(None),
        headers={"Authorization": f"Bearer {None}"}
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_delete_favourites(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config={data_from_resp_favourites['name_config']}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp_del = resp.json()

    # Verify the response
    assert resp.status_code == 200
    assert data_from_resp_del == 'favourites deleted'


async def test_delete_favourites_fail_another_name_config(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config=dcf512d6-7829-4769-a5a3-ebd255c558ab",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration with this name does not exist."}'


async def test_delete_favourites_fail_no_name_config(client):
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
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid",' \
                           b'"type":"type_error.uuid"}]}'


async def test_delete_favourites_fail_no_token(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config={data_from_resp_favourites['name_config']}",
        headers={"Authorization": f"Bearer {None}"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_delete_favourites_fail_no_config_and_token(client):
    # Send the request with authentication token
    resp = client.delete(
        f"/favourites/?name_config=None",
        headers={"Authorization": f"Bearer {None}"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_get_all_favourites(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client,
                                                                                            google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/all",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_favourites_all = resp.json()

    assert resp.status_code == 200
    assert str(data_from_resp_favourites['name_config']) == (dict(data_favourites_all[0]))['name_config']
    assert data_from_resp_favourites['name_esphome'] == (dict(data_favourites_all[0]))['name_esphome']


async def test_get_all_favourites_two_favourites(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client,
                                                                                            google_profile_one,
                                                                                            config_data,
                                                                                            config_data_two)
    data_from_resp_favourites = data_from_resp_favourites_list[0]
    data_from_resp_favourites_two = data_from_resp_favourites_list[1]

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/all",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_favourites_all = resp.json()

    assert resp.status_code == 200
    assert str(data_from_resp_favourites['name_config']) == (dict(data_favourites_all[0]))['name_config']
    assert data_from_resp_favourites['name_esphome'] == (dict(data_favourites_all[0]))['name_esphome']
    assert str(data_from_resp_favourites_two['name_config']) == (dict(data_favourites_all[1]))['name_config']
    assert data_from_resp_favourites_two['name_esphome'] == (dict(data_favourites_all[1]))['name_esphome']


async def test_failed_get_all_favourites_fail_no_token(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client,
                                                                                            google_profile_one,
                                                                                            config_data,
                                                                                            config_data_two)
    # Send the request with authentication token
    resp = client.get(
        f"/favourites/all",
        headers={"Authorization": f"Bearer {None}"}
    )

    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_get_one_favourites(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={data_from_resp_favourites['name_config']}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 201
    assert config_data == data_from_resp['json_text']


async def test_get_one_favourites_fail_no_favourites_but_save_config(client):
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
    os.remove(f'{UPLOADED_FILES_PATH}{data_config_one["name_config"]}.yaml')


async def test_get_one_favourites_fail_no_config(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config=None",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # Verify the response
    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid",' \
                           b'"type":"type_error.uuid"}]}'


async def test_get_one_favourites_fail_no_token(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={data_from_resp_favourites['name_config']}",
        headers={"Authorization": f"Bearer {None}"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_get_one_favourites_fail_non_existent_token(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.get(
        f"/favourites/one?name_config={data_from_resp_favourites['name_config']}",
        headers={"Authorization": f"Bearer vyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                                  f".eyJzdWIiOiJ0cm9sb2xvMTIwMTIwQGdtYWlsLmNvbSIsImV4cCI6MTY5MTU3MTc4MX0"
                                  f".O7Fd_xP4hlxF0IrY483NlFotlqbyUxjZJJzoE698Fk8"}
    )

    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'


async def test_get_edit_favourites(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_from_resp_favourites['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 200
    # Favorites changed
    assert data_from_resp_favourites['user_id'] == data_from_resp['user_id']
    assert str(data_from_resp_favourites['name_config']) != data_from_resp['name_config']
    assert data_from_resp_favourites['name_esphome'] != data_from_resp['name_esphome']
    assert data_from_resp_favourites['id'] != data_from_resp['id']


async def test_get_edit_favourites_to_another_existing_favorites(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client,
                                                                                            google_profile_one,
                                                                                            config_data,
                                                                                            config_data_two)
    data_from_resp_favourites = data_from_resp_favourites_list[0]
    data_from_resp_favourites_two = data_from_resp_favourites_list[1]

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_from_resp_favourites['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    data_from_resp = resp.json()

    # Verify the response
    assert resp.status_code == 200
    # Favorites changed
    assert data_from_resp_favourites['user_id'] == data_from_resp['user_id']
    assert str(data_from_resp_favourites['name_config']) != data_from_resp['name_config']
    assert data_from_resp_favourites['name_esphome'] != data_from_resp['name_esphome']
    assert data_from_resp_favourites['id'] != data_from_resp['id']

    assert data_from_resp_favourites_two['user_id'] == data_from_resp['user_id']
    assert str(data_from_resp_favourites_two['name_config']) == data_from_resp['name_config']
    assert data_from_resp_favourites_two['name_esphome'] == data_from_resp['name_esphome']
    assert data_from_resp_favourites_two['id'] == data_from_resp['id']


async def test_get_edit_favourites_fail_none_data(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_from_resp_favourites['name_config']}",
        data=json.dumps(None),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"Configuration was not sent"}'


async def test_get_edit_favourites_fail_no_data(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_from_resp_favourites['name_config']}",
        data=json.dumps({}),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 404
    assert resp.content == b'{"message":"esphhome name item not filled"}'


async def test_get_edit_favourites_fail_none_name_config(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config=None",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {access_token}"}
    )
    # Verify the response
    assert resp.status_code == 422
    assert resp.content == b'{"detail":[{"loc":["query","name_config"],"msg":"value is not a valid uuid",' \
                           b'"type":"type_error.uuid"}]}'


async def test_get_edit_favourites_file_no_token(client):
    access_token, data_from_resp_favourites_list = await authenticate_and_create_favourites(client, google_profile_one,
                                                                                            config_data)
    data_from_resp_favourites = data_from_resp_favourites_list[0]

    # Send the request with authentication token
    resp = client.post(
        f"/favourites/edit?name_config={data_from_resp_favourites['name_config']}",
        data=json.dumps(config_data_two),
        headers={"Authorization": f"Bearer {None}"}
    )
    # Verify the response
    assert resp.status_code == 401
    assert resp.content == b'{"detail":"Could not validate credentials"}'
