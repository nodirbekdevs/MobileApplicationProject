from pydantic import BaseModel


class AuthenticationSchema(BaseModel):
    phone_number: str
    password: str
