from jwt import encode, decode
from base64 import b64decode
from asyncio import to_thread

from ..utils import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_HOURS
from ..services import Time


class Token(object):
    @classmethod
    async def encode_jwt(cls, data: dict):
        lifetime = await to_thread(Time().make_lifetime, TOKEN_EXPIRE_HOURS)
        data['expires'] = lifetime
        access_token = await to_thread(encode, payload=data, key=SECRET_KEY, algorithm=ALGORITHM)
        return dict(token=access_token)

    @classmethod
    async def decode(cls, token: str):
        return await to_thread(decode, jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])

    @classmethod
    async def decode_jwt(cls, token: str):
        decoded_token = await to_thread(decode, jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        checking_time = await to_thread(Time().lifetime_checking, decoded_token["expires"])

        return None if checking_time is None else decoded_token

    @classmethod
    async def decode_base_64(cls, token: str):
        decoded_token = await to_thread(b64decode, s=token)
        return decoded_token.decode('utf-8').split(':')
