import pydantic


class LoginDetails(pydantic.BaseModel):
    Username: str
    Password: str


class LoginReturn(pydantic.BaseModel):
    token: str


class UserSetType(pydantic.BaseModel):
    type: int


class UserSetTypeReturn(pydantic.BaseModel):
    ...