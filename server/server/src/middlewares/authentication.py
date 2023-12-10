from fastapi import Request, HTTPException, Query

from ..utils import AUTH_USERNAME, AUTH_PASSWORD
from ..services import Token


class Authentication(object):
    def __init__(self, required_roles: list):
        self.required_roles = required_roles

    async def __call__(self, request: Request):
        token, decoded_token = request.headers.get('Authorization'), dict()

        if not token:
            raise HTTPException(status_code=403, detail='Unauthorized')

        token_type, token = token.split(' ')

        tokenization = Token()

        if token_type == 'Basic':
            decoded_credentials = await tokenization.decode_base_64(token=token)
            username, password = decoded_credentials[0], decoded_credentials[1]

            if username != AUTH_USERNAME or password != AUTH_PASSWORD:
                raise HTTPException(status_code=403, detail="You have not had permission")

            params = dict(request.query_params)

            decoded_token = dict(id=int(params['id']) if params.get('id') else None, role=params.get('role'))

            # if 'id' in params:
            #     del params['id']
            # del params['role']
            #
            # request.query_params = params

        if token_type == 'Bearer':
            decoded_token = await tokenization.decode_jwt(token)

        if decoded_token is None:
            raise HTTPException(status_code=403, detail="Token lifetime expired")

        if decoded_token['role'] not in self.required_roles:
            raise HTTPException(status_code=403, detail='Access denied')

        request.state.user = decoded_token

        return request
