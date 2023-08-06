import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, Optional

import aiohttp
import jwt
from cryptography.hazmat.backends.openssl.rsa import _RSAPublicKey
from jwt.algorithms import RSAAlgorithm
from pydantic import ValidationError

from .entities import JwtAccessToken

__all__ = ()

logger = logging.getLogger(__name__)


DEFAULT_JWKS_RESPONSE_CACHE_PERIOD = 3600  # 1 hour


class Oauth2JwtAccessTokenValidator:
    """Parses and validates JWT-format OAuth2 access tokens against a JWKS endpoint

    Fetches public keys from the provided JWKS endpoint which is used to verify
    the validity of the access token.

    Only supports the RS256 algorithm.

    The public keys from the JWKS endpoint are cached for one hour by default, to
    minimize the number of external requests that have to be made.

    Not ready to use until it's been initialized  via the `init` method.
    """

    def __init__(self):
        self._jwks_url = None
        self._audiences = None
        self._jwks_kid_mapping = None
        self._jwks_cache_period = DEFAULT_JWKS_RESPONSE_CACHE_PERIOD
        self._jwks_cached_at = None

    def init(
        self,
        jwks_url: str,
        audiences: Iterable[str],
        *,
        jwks_cache_period: int = DEFAULT_JWKS_RESPONSE_CACHE_PERIOD,
    ):
        """Set up Oauth 2.0 JWT validation

        Args:
            jwks_url:
                The JWKS endpoint to fetch the public keys from. Usually in the
                format: "https://domain/.well-known/jwks.json"
            audiences:
                Accepted `aud` values for incoming access tokens
            jwks_cache_period:
                How many seconds to cache the JWKS response. Defaults to 1 hour.
        """

        self._jwks_url = jwks_url
        self._jwks_cache_period = jwks_cache_period
        self._audiences = list(audiences)

    def is_configured(self) -> bool:
        return bool(self._jwks_url)

    async def parse(self, access_token: str) -> Optional[JwtAccessToken]:
        """Parse the supplied JWT-formatted access token

        Returns a parsed JwtAccessToken object on successful verification,
        otherwise `None`.
        """
        if not self.is_configured():
            logger.info("JWT Access Token validator is not set up!")
            return None

        if not access_token:
            logger.debug("No JWT token provided")
            return None

        try:
            unverified_header = jwt.get_unverified_header(access_token)
        except jwt.InvalidTokenError as ex:
            logger.debug(f"Decoding unverified JWT token failed with error: {ex!r}")
            return None

        try:
            token_kid = unverified_header["kid"]
        except KeyError:
            logger.debug("No `kid` found in JWT token")
            return None

        try:
            public_key = await self._get_public_key(token_kid)
        except KeyError:
            logger.debug("No matching kid for JWT token")
            return None

        try:
            decoded = self._decode_jwt_token(public_key, access_token)
        except jwt.InvalidTokenError as ex:
            logger.debug(f"Decoding verified JWT token failed with error: {ex!r}")
            return None

        try:
            parsed_access_token = JwtAccessToken(**decoded, raw=access_token)
        except ValidationError as ex:
            logger.debug(f"Failed to parse JWT token with validation error: {ex!r}")
            return None

        return parsed_access_token

    async def _get_public_key(self, kid: str) -> _RSAPublicKey:
        mapping = await self._get_jwks_kid_mapping()
        return mapping[kid]

    async def _get_jwks_kid_mapping(self) -> Dict[str, _RSAPublicKey]:
        if self._jwks_cached_at is None or (
            (datetime.utcnow() - self._jwks_cached_at)
            > timedelta(seconds=self._jwks_cache_period)
        ):
            jwks_data = await self._fetch_jwks_data()
            self._jwks_kid_mapping = {
                k["kid"]: RSAAlgorithm.from_jwk(json.dumps(k))
                for k in jwks_data["keys"]
                if k["kty"] == "RSA" and k["alg"] == "RS256"
            }
            self._jwks_cached_at = datetime.utcnow()
            assert len(self._jwks_kid_mapping) > 0

        return self._jwks_kid_mapping

    async def _fetch_jwks_data(self):
        timeout = aiohttp.ClientTimeout(total=10)

        logger.info(f"Fetching JWKS data from {self._jwks_url}")

        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(self._jwks_url) as response:
                try:
                    return await response.json()
                except Exception as ex:
                    raise RuntimeError(f"Failed to load JWKS data with exception: {ex}")

    def _decode_jwt_token(
        self, public_key: _RSAPublicKey, access_token: str
    ) -> Dict[str, Any]:
        # NOTE: jwt.decode has erroneously set key: str
        return jwt.decode(access_token, key=public_key, audience=self._audiences, algorithms=["RS256"])  # type: ignore
