import datetime
import jwt

from .service_account import ServiceAccount

JWT_ALGORITHM = 'RS256'


class JWTHandler:
    _service_account: ServiceAccount
    _audience: str
    _seconds_before_expire: int

    def __init__(self, service_account: ServiceAccount, seconds_before_expire: int, audience: str) -> None:
        self._service_account = service_account
        self._audience = audience
        self._seconds_before_expire = seconds_before_expire

    def generate_token(self) -> str:
        now = datetime.datetime.utcnow()

        return jwt.encode(
            {
                'iss': self._service_account.client_email,
                'sub': self._service_account.client_email,
                'aud': self._audience,
                'iat': now,
                'exp': now + datetime.timedelta(hours=1),
            },
            self._service_account.private_key,
            algorithm=JWT_ALGORITHM,
            headers={
                'kid': self._service_account.private_key_id,
                'typ': 'JWT',
                'alg': JWT_ALGORITHM,
            })

    def is_token_expired(self, token: str) -> bool:
        decoded = jwt.decode(token,
                             self._service_account.private_key,
                             algorithms=JWT_ALGORITHM,
                             options={"verify_signature": False})
        exp_time = datetime.datetime.utcfromtimestamp(decoded['exp'])

        if exp_time - datetime.datetime.utcnow() < datetime.timedelta(seconds=self._seconds_before_expire):
            return True
        return False
