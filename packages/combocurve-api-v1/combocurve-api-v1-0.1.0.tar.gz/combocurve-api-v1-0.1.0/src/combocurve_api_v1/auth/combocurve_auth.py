from .service_account import ServiceAccount
from .token_refresher import TokenRefresher

DEFAULT_AUDIENCE = 'https://api.combocurve.com'


class ComboCurveAuth:
    _token_refresher: TokenRefresher
    _api_key: str

    def __init__(self,
                 service_account: ServiceAccount,
                 api_key: str,
                 seconds_before_token_expire: int = 60,
                 audience: str = DEFAULT_AUDIENCE) -> None:
        self._token_refresher = TokenRefresher(service_account, seconds_before_token_expire, audience)
        self._api_key = api_key

    def get_auth_headers(self):
        token = self._token_refresher.get_access_token()
        return {'Authorization': f'Bearer {token}', 'x-api-key': self._api_key}
