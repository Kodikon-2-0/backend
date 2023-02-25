import datetime

import bcrypt
import jwt
from fastapi import HTTPException

import db as database

JWT_KEY = "changeme"


def login(username: str, password: str) -> str:
    db = database.get_db()
    cur = db.cursor()
    cur.execute("SELECT username, password, userid FROM user WHERE username = ?", (username,))
    result = cur.fetchone()
    if not result:
        print("hi")
        raise HTTPException(status_code=403, detail="Invalid Username/Password")

    state = bcrypt.checkpw(password.encode(encoding="utf-8"), bytes.fromhex(result[1]))
    if not state:
        raise HTTPException(status_code=403, detail="Invalid Username/Password")
    return jwt.encode({"exp": datetime.datetime.utcnow().replace(hour=(datetime.datetime.utcnow().hour + 5)),
                       "userid": result[2]}, key=JWT_KEY, algorithm="HS256")


def create_account(username: str, password: str) -> str:
    db = database.get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO user(username, password) VALUES (?, ?)",
                (username, bcrypt.hashpw(password.encode(encoding="utf-8"), bcrypt.gensalt()).hex(),))
    db.commit()
    return str(cur.lastrowid)


def set_user_type(userid: int, newtype: int) -> None:
    ...


def get_user_from_token(token: str) -> int:
    obj = jwt.decode(token, key=JWT_KEY, algorithms=["HS256"])
    return obj['userid']


def set_user_type(usertype: int, user: int) -> dict:
    db = database.get_db()
    cur = db.cursor()
    cur.execute("SELECT usertype from user WHERE userid = ?", (user,))
    cur_type = cur.fetchone()[0]
    if (cur_type & 4) ^ (usertype & 4):
        raise HTTPException(status_code=403, detail="Cannot set admin bit")

    cur.execute("UPDATE user SET usertype = ? WHERE userid = ?", (usertype, user,))
    db.commit()
    return {}
