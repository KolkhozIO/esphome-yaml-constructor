import json

from jose import jwt

import settings
from tests.settings_tests import google_profile_one, google_profile_two


async def test_googleauth_endpoint_get_bin(client, get_user_from_database):
    resp = client.post("/google/login", json=google_profile_one)
    data_from_resp = resp.json()

    config_from_db = await get_user_from_database(google_profile_one['email'])
    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 200
    assert config_from_db['user_id'] == google_profile_one['googleId']
    assert config_from_db['name'] == google_profile_one['familyName']
    assert config_from_db['surname'] == google_profile_one['givenName']
    assert config_from_db['email'] == google_profile_one['email']
    assert config_from_db['is_active'] is True

    payload = jwt.decode(
        data_from_resp['access_token'], settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email: str = payload.get("sub")

    assert config_from_db['email'] == email
    assert google_profile_one['email'] == email


async def test_googleauth_endpoint_get_bin_two(client, get_user_from_database, create_test_user):
    test_user = await create_test_user(**{
        'user_id': google_profile_one['googleId'],
        'name': google_profile_one['familyName'],
        'surname': google_profile_one['givenName'],
        'email': google_profile_one['email'],
        'is_active': True,
    })
    assert len(test_user) == 1
    test_user = dict(test_user[0])

    resp = client.post("/google/login", json=google_profile_one)
    data_from_resp = resp.json()

    config_from_db = await get_user_from_database(google_profile_one['email'])
    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    assert resp.status_code == 200
    assert config_from_db['user_id'] == google_profile_one['googleId']
    assert config_from_db['name'] == google_profile_one['familyName']
    assert config_from_db['surname'] == google_profile_one['givenName']
    assert config_from_db['email'] == google_profile_one['email']
    assert config_from_db['is_active'] is True
    assert config_from_db['user_id'] == test_user['user_id']
    assert config_from_db['name'] == test_user['name']
    assert config_from_db['surname'] == test_user['surname']
    assert config_from_db['email'] == test_user['email']

    payload = jwt.decode(
        data_from_resp['access_token'], settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email: str = payload.get("sub")

    assert config_from_db['email'] == email
    assert google_profile_one['email'] == email


async def test_googleauth_endpoint_get_bin_three(client, get_user_from_database):
    resp = client.post("/google/login", json=json.dumps(None))
    config_from_db = await get_user_from_database(google_profile_one['email'])

    assert len(config_from_db) == 0
    assert resp.status_code == 404
    assert resp.content == b'{"message":"No user information received from google"}'
    assert resp.headers == [(b'content-length', b'54'), (b'content-type', b'application/json')]


async def test_googleauth_endpoint_get_bin_four(client):
    resp = client.post("/google/login", json={})

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Missing required keys: googleId, familyName, givenName, email"}'
    assert resp.headers == [(b'content-length', b'75'), (b'content-type', b'application/json')]


async def test_googleauth_endpoint_get_bin_five(client, get_user_from_database):
    resp = client.post("/google/login", json=google_profile_two)
    config_from_db = await get_user_from_database(google_profile_two['email'])

    assert len(config_from_db) == 0
    assert resp.status_code == 404
    assert resp.content == b'{"message":"Missing required keys: googleId"}'
    assert resp.headers == [(b'content-length', b'45'), (b'content-type', b'application/json')]

