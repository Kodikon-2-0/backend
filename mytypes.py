import typing

import pydantic


class LoginDetails(pydantic.BaseModel):
    Username: str
    Password: str


class CreateAccountDetails(LoginDetails):
    permissions: int


class LoginReturn(pydantic.BaseModel):
    token: str
    usertype: int


class UserSetType(pydantic.BaseModel):
    type: int


class UserSetTypeReturn(pydantic.BaseModel):
    ...


class Info(pydantic.BaseModel):
    names: typing.List[str]
