import json

from jose import jwt

import settings
from tests.settings_tests import google_profile_one, google_profile_two


async def test_googleauth_endpoint_get_bin(client):
    resp = client.post("/google/login", json=google_profile_one)
    data_from_resp = resp.json()

    payload = jwt.decode(
        data_from_resp['access_token'], settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email: str = payload.get("sub")

    assert resp.status_code == 200
    assert google_profile_one['email'] == email


async def test_googleauth_endpoint_get_bin_two(client):
    # Create google user one
    resp = client.post("/google/login", json=google_profile_one)
    assert resp.status_code == 200
    data_from_resp_one = resp.json()

    payload = jwt.decode(
        data_from_resp_one['access_token'], settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email_one: str = payload.get("sub")

    # Create google user two
    resp = client.post("/google/login", json=google_profile_one)
    data_from_resp_two = resp.json()

    payload = jwt.decode(
        data_from_resp_two['access_token'], settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email_two: str = payload.get("sub")

    assert resp.status_code == 200
    assert google_profile_one['email'] == email_one
    assert google_profile_one['email'] == email_two
    assert email_one == email_two
    assert data_from_resp_one == data_from_resp_two


async def test_googleauth_endpoint_get_bin_three(client):
    resp = client.post("/google/login", json=json.dumps(None))

    assert resp.status_code == 404
    assert resp.content == b'{"message":"No user information received from google"}'


async def test_googleauth_endpoint_get_bin_four(client):
    resp = client.post("/google/login", json={})

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Missing required keys: googleId, familyName, givenName, email"}'


async def test_googleauth_endpoint_get_bin_five(client):
    resp = client.post("/google/login", json=google_profile_two)

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Missing required keys: googleId"}'
