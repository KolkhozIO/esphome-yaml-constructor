import json

from jose import jwt

import settings
from tests.settings_tests import google_profile_one, google_profile_two


async def create_google_user_and_decode_token(client, google_profile):
    resp = client.post("/google/login", json=google_profile)
    assert resp.status_code == 200
    data_from_resp_google = resp.json()

    payload = jwt.decode(
        data_from_resp_google['access_token'], settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    email: str = payload.get("sub")
    return data_from_resp_google, email


async def test_googleauth_endpoint(client):
    data_from_resp_google, email = await create_google_user_and_decode_token(client, google_profile_one)
    assert google_profile_one['email'] == email


async def test_googleauth_endpoint_two_authorizations(client):
    data_from_resp_google_one, email_one = await create_google_user_and_decode_token(client, google_profile_one)
    data_from_resp_google_two, email_two = await create_google_user_and_decode_token(client, google_profile_one)

    assert google_profile_one['email'] == email_one
    assert google_profile_one['email'] == email_two
    assert email_one == email_two
    assert data_from_resp_google_one == data_from_resp_google_two


async def test_googleauth_endpoint_fail_none_profile(client):
    resp = client.post("/google/login", json=json.dumps(None))

    assert resp.status_code == 404
    assert resp.content == b'{"message":"No user information received from google"}'


async def test_googleauth_endpoint_fail_no_profile(client):
    resp = client.post("/google/login", json={})

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Missing required keys: googleId, familyName, givenName, email"}'


async def test_googleauth_endpoint_fail_bed_profile(client):
    resp = client.post("/google/login", json=google_profile_two)

    assert resp.status_code == 404
    assert resp.content == b'{"message":"Missing required keys: googleId"}'
