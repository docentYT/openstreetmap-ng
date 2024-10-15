import pytest
from authlib.integrations.httpx_client import AsyncOAuth2Client
from httpx import AsyncClient
from starlette import status

from app.config import APP_URL
from app.lib.buffered_random import buffered_rand_urlsafe


async def test_openid_configuration(client: AsyncClient):
    r = await client.get('/.well-known/openid-configuration')
    assert r.is_success, r.text

    config = r.json()
    assert config['issuer'] == APP_URL
    assert config['authorization_endpoint'] == f'{APP_URL}/oauth2/authorize'
    assert config['token_endpoint'] == f'{APP_URL}/oauth2/token'


async def test_authorize_invalid_system_app(client: AsyncClient):
    client.headers['Authorization'] = 'User user1'
    auth_client = AsyncOAuth2Client(
        base_url=client.base_url,
        transport=client._transport,  # noqa: SLF001
        client_id='SystemApp.web',
        client_secret='',
        scope='',
        redirect_uri='urn:ietf:wg:oauth:2.0:oob',
    )
    authorization_url, _ = auth_client.create_authorization_url('/oauth2/authorize')

    r = await client.post(authorization_url)
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.json()['detail'] == 'Invalid client ID'


@pytest.mark.parametrize(
    'token_endpoint_auth_method',
    [
        'client_secret_post',
        'client_secret_basic',
    ],
)
async def test_authorize_token_oob(client: AsyncClient, token_endpoint_auth_method: str):
    client.headers['Authorization'] = 'User user1'
    auth_client = AsyncOAuth2Client(
        base_url=client.base_url,
        transport=client._transport,  # noqa: SLF001
        client_id='testapp',
        client_secret='testapp.secret',  # noqa: S106
        scope='',
        redirect_uri='urn:ietf:wg:oauth:2.0:oob',
        code_challenge_method='S256',
        token_endpoint_auth_method=token_endpoint_auth_method,
    )
    code_verifier = buffered_rand_urlsafe(48)
    authorization_url, state = auth_client.create_authorization_url('/oauth2/authorize', code_verifier=code_verifier)

    r = await client.post(authorization_url)
    assert r.is_success, r.text

    authorization_code = r.headers['Test-OAuth2-Authorization-Code']
    authorization_code, _, state_response = authorization_code.partition('#')
    assert state == state_response

    data: dict = await auth_client.fetch_token(
        '/oauth2/token',
        grant_type='authorization_code',
        auth=('testapp', 'testapp.secret'),
        code=authorization_code,
        code_verifier=code_verifier,
    )
    assert data['access_token']
    assert data['token_type'] == 'Bearer'  # noqa: S105
    assert data['scope'] == ''
    assert data['created_at']

    r = await auth_client.get('/api/0.6/user/details.json')
    assert r.is_success, r.text

    user = r.json()['user']
    assert user['display_name'] == 'user1'