import logging
from typing import NotRequired, TypedDict

import orjson

from app.config import OPENID_DISCOVERY_HTTP_TIMEOUT
from app.lib.crypto import hash_storage_key
from app.services.cache_service import CacheContext, CacheService
from app.utils import HTTP

_CTX = CacheContext('OpenID')


class OpenIDDiscovery(TypedDict):
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    introspection_endpoint: NotRequired[str]
    userinfo_endpoint: str
    revocation_endpoint: str
    jwks_uri: str
    scopes_supported: list[str]
    response_types_supported: list[str]
    response_modes_supported: list[str]
    grant_types_supported: list[str]
    code_challenge_methods_supported: list[str]
    token_endpoint_auth_methods_supported: list[str]
    subject_types_supported: list[str]
    id_token_signing_alg_values_supported: list[str]
    claim_types_supported: list[str]
    claims_supported: list[str]


class OpenIDQuery:
    @staticmethod
    async def discovery(base_url: str) -> OpenIDDiscovery:
        """Perform OpenID Connect discovery."""

        async def factory() -> bytes:
            logging.debug('OpenID discovery cache miss for %r', base_url)
            r = await HTTP.get(
                f'{base_url}/.well-known/openid-configuration',
                timeout=OPENID_DISCOVERY_HTTP_TIMEOUT.total_seconds(),
            )
            r.raise_for_status()
            return r.content

        key = hash_storage_key(base_url, '.json')
        content = await CacheService.get(
            key, _CTX, factory, ttl=OPENID_DISCOVERY_HTTP_TIMEOUT
        )
        return orjson.loads(content)
