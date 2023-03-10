import json
from urllib import parse

import fastapi
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import auth
import mytypes as types
import resource_groups
import resources

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return auth.get_user_from_token(token)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": auth.login(form_data.username, form_data.password)[0], "token_type": "bearer"}


@app.post("/login", response_model=types.LoginReturn)
async def login(details: types.LoginDetails):
    auth_token, user_type = auth.login(username=details.Username, password=details.Password)
    return types.LoginReturn(token=auth_token, usertype=user_type)


@app.post("/createAccount", response_model=types.CreateAccountResult)
async def create_account(details: types.CreateAccountDetails):
    return types.CreateAccountResult(userid=auth.create_account(username=details.Username, password=details.Password,
                                                                permissions=details.permissions))


@app.patch("/user/setType", response_model=types.UserSetTypeReturn)
async def set_type(new_type: types.UserSetType, user: int = Depends(get_current_user)):
    return auth.set_user_type(new_type.type, user)


@app.get("/data/{state}/{district}/mandals", response_model=types.Info)
async def get_mandal_info(state, district):
    with open("data.json") as fp:
        data = json.load(fp)
    state = parse.unquote(state)
    district = parse.unquote(district)
    if state in data and district in data[state]:
        return types.Info(names=data[state][district])
    else:
        raise fastapi.HTTPException(status_code=404, detail="Not found")


@app.get("/data/{state}/districts", response_model=types.Info)
async def get_district_info(state):
    with open("data.json") as fp:
        data = json.load(fp)
    state = parse.unquote(state)
    if state in data:
        return types.Info(names=[name for name in data[state]])
    else:
        raise fastapi.HTTPException(status_code=404, detail="Not found")


@app.get("/data/states", response_model=types.Info)
async def get_state_info():
    with open("data.json") as fp:
        data = json.load(fp)
    return types.Info(names=[name for name in data])


@app.post("/data/{state}/{district}/{mandal}/search", response_model=types.SearchResult)
async def search(state: str, district: str, mandal: str, details: types.SearchDetails):
    rv = resources.search(state, district, mandal, details.start_time, details.end_time, details.resource_type)
    return types.SearchResult(results=rv)


@app.get("/data/resourceGroups", response_model=types.ResourceGroupReturn)
async def get_resource_groups():
    return types.ResourceGroupReturn(resource_groups=resource_groups.list_groups())


@app.post("/data/{state}/{district}/{mandal}/resources", response_model=types.CreateResourceResult)
async def create_resource(state: str, district: str, mandal: str, details: types.ResourceCreateDetails,
                          user: int = Depends(get_current_user)):
    return types.CreateResourceResult(
        id=resources.create(state, district, mandal, details.resource_group_id, details.data, user))


@app.post("/order")
async def create_order(details: types.OrderCreateDetails, user: int = Depends(get_current_user)):
    return resources.order(details.resource_id, user, details.from_time, details.to_time, details.quantity)


@app.post("/resources/{resource_id}/setAvailableRange")
async def set_resource_range(resource_id: int, details: types.ResourceAvailabilityDetails,
                             user: int = Depends(get_current_user)):
    resources.set_available_range(resource_id, details.start, details.end, user)


@app.get("/orders", response_model=types.OrderBookResults)
async def get_orders(user_id: int = Depends(get_current_user)):
    return types.OrderBookResults(orders=resources.get_orders(user_id))


@app.patch("/order/{order_id}")
async def update_order(order_id: int, details: types.OrderAcceptInfo, user: int = Depends(get_current_user)):
    resources.update_order(user, order_id, details.new_status)
