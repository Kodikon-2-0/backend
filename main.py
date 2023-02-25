from fastapi import FastAPI

import auth
import mytypes as types

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login", response_model=types.LoginReturn)
async def login(details: types.LoginDetails):
    return types.LoginReturn(token=auth.login(username=details.Username, password=details.Password))


@app.post("/createAccount", response_model=types.LoginReturn)
async def create_account(details: types.LoginDetails):
    return types.LoginReturn(token=auth.create_account(username=details.Username, password=details.Password))
