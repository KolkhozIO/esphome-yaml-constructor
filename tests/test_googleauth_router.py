import json

from jose import jwt

import settings


async def test_googleauth_endpoint_get_bin(client, create_config_in_database, get_user_from_database):

    profile = {
        'googleId': '105383501433443125091',
        'imageUrl': 'https://lh3.googleusercontent.com/a/AAcHTtdvp_AKqaxgAaouTOHTeYbmoG48KMbTwo-KlLxuBks3_GM=s96-c',
        'email': 'trololo120120@gmail.com',
        'name': 'Великий Алба',
        'givenName': 'Великий',
        'familyName': 'Алба'
    }

    resp = client.post("/google/login", json=profile)
    data_from_resp = resp.json()

    config_from_db = await get_user_from_database(profile['email'])
    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    # Проверить код состояния ответа
    assert resp.status_code == 200
    assert config_from_db['user_id'] == profile['googleId']
    assert config_from_db['name'] == profile['familyName']
    assert config_from_db['surname'] == profile['givenName']
    assert config_from_db['email'] == profile['email']
    assert config_from_db['is_active'] is True

    payload = jwt.decode(
        data_from_resp['access_token'], settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email: str = payload.get("sub")

    assert config_from_db['email'] == email
    assert profile['email'] == email


async def test_googleauth_endpoint_get_bin_two(client, create_config_in_database, get_user_from_database, create_test_user):

    profile = {
        'googleId': '105383501433443125091',
        'imageUrl': 'https://lh3.googleusercontent.com/a/AAcHTtdvp_AKqaxgAaouTOHTeYbmoG48KMbTwo-KlLxuBks3_GM=s96-c',
        'email': 'trololo120120@gmail.com',
        'name': 'Великий Алба',
        'givenName': 'Великий',
        'familyName': 'Алба'
    }

    test_user = await create_test_user(**{
        'user_id': profile['googleId'],
        'name': profile['familyName'],
        'surname': profile['givenName'],
        'email': profile['email'],
        'is_active': True,
    })
    assert len(test_user) == 1
    test_user = dict(test_user[0])

    resp = client.post("/google/login", json=profile)
    data_from_resp = resp.json()

    config_from_db = await get_user_from_database(profile['email'])
    assert len(config_from_db) == 1
    config_from_db = dict(config_from_db[0])

    # Проверить код состояния ответа
    assert resp.status_code == 200
    assert config_from_db['user_id'] == profile['googleId']
    assert config_from_db['name'] == profile['familyName']
    assert config_from_db['surname'] == profile['givenName']
    assert config_from_db['email'] == profile['email']
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
    assert profile['email'] == email


async def test_googleauth_endpoint_get_bin_three(client, create_config_in_database, get_user_from_database):
    profile = {
        'googleId': '105383501433443125091',
        'imageUrl': 'https://lh3.googleusercontent.com/a/AAcHTtdvp_AKqaxgAaouTOHTeYbmoG48KMbTwo-KlLxuBks3_GM=s96-c',
        'email': 'trololo120120@gmail.com',
        'name': 'Великий Алба',
        'givenName': 'Великий',
        'familyName': 'Алба'
    }

    resp = client.post("/google/login", json=json.dumps(None))

    config_from_db = await get_user_from_database(profile['email'])
    assert len(config_from_db) == 0

    # Проверить код состояния ответа
    assert resp.status_code == 404
    assert resp.content == b'{"message":"No user information received from google"}'
    assert resp.headers == [(b'content-length', b'54'), (b'content-type', b'application/json')]


async def test_googleauth_endpoint_get_bin_four(client, create_config_in_database, get_user_from_database):
    resp = client.post("/google/login", json={})

    # Проверить код состояния ответа
    assert resp.status_code == 404
    assert resp.content == b'{"detail":"Missing required keys: googleId, familyName, givenName, email"}'
    assert resp.headers == [(b'content-length', b'74'), (b'content-type', b'application/json')]


async def test_googleauth_endpoint_get_bin_five(client, create_config_in_database, get_user_from_database):
    profile = {
        'imageUrl': 'https://lh3.googleusercontent.com/a/AAcHTtdvp_AKqaxgAaouTOHTeYbmoG48KMbTwo-KlLxuBks3_GM=s96-c',
        'email': 'trololo120120@gmail.com',
        'name': 'Великий Алба',
        'givenName': 'Великий',
        'familyName': 'Алба'
    }

    resp = client.post("/google/login", json=profile)

    config_from_db = await get_user_from_database(profile['email'])
    assert len(config_from_db) == 0

    # Проверить код состояния ответа
    assert resp.status_code == 404
    assert resp.content == b'{"detail":"Missing required keys: googleId"}'
    assert resp.headers == [(b'content-length', b'44'), (b'content-type', b'application/json')]

