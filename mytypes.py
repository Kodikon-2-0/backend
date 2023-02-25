import pydantic


class LoginDetails(pydantic.BaseModel):
    Username: str
    Password: str


class LoginReturn(pydantic.BaseModel):
    token: str
