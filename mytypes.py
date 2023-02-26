import datetime
import typing

import pydantic


class LoginDetails(pydantic.BaseModel):
    Username: str
    Password: str


class CreateAccountDetails(LoginDetails):
    permissions: int


class CreateAccountResult(pydantic.BaseModel):
    userid: str
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
    start_time: datetime.datetime
    end_time: datetime.datetime
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


class ResourceAvailabilityDetails(pydantic.BaseModel):
    start: datetime.datetime
    end: datetime.datetime


class SearchResultsInfo(pydantic.BaseModel):
    resource_id: int
    owner: int
    state: str
    district: str
    mandal: str
    data: str
    available_from: datetime.datetime
    available_till: datetime.datetime


class SearchResult(pydantic.BaseModel):
    results: typing.List[SearchResultsInfo]


class CreateResourceResult(pydantic.BaseModel):
    id: int


class OrderInfo(pydantic.BaseModel):
    orderid: int
    lessor: str
    lessee: str
    resource: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    quantity: float
    order_status: int
    resource_group: int


class OrderBookResults(pydantic.BaseModel):
    orders: typing.List[OrderInfo]


class OrderAcceptInfo(pydantic.BaseModel):
    new_status: int

