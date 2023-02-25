import datetime
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


class SearchDetails(pydantic.BaseModel):
    start_time: int
    end_time: int
    resource_type: int


class ResourceGroupInfo(pydantic.BaseModel):
    name: str
    id: int
    unit: str


class ResourceGroupReturn(pydantic.BaseModel):
    resource_groups: typing.List[ResourceGroupInfo]


class ResourceCreateDetails(pydantic.BaseModel):
    resource_group_id: int
    data: str


class OrderCreateDetails(pydantic.BaseModel):
    resource_id: int
    from_time: datetime.datetime
    to_time: datetime.datetime
    quantity: float
