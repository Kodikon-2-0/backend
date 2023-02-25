import datetime

from fastapi import HTTPException
import jwt
import db as database
import bcrypt


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
                       "userid": result[2]}, key="changeme")


def create_account(username: str, password: str) -> str:
    db = database.get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO user(username, password) VALUES (?, ?)",
                (username, bcrypt.hashpw(password.encode(encoding="utf-8"), bcrypt.gensalt()).hex(),))
    db.commit()
    return str(cur.lastrowid)
