from asyncio import to_thread

from passlib.hash import pbkdf2_sha256


class Bcrypt(object):
    @staticmethod
    async def hash(password):
        return await to_thread(pbkdf2_sha256.hash, password)

    @staticmethod
    async def check(hashed_password, password):
        return await to_thread(pbkdf2_sha256.verify, password, hashed_password)
