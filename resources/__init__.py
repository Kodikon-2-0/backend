import datetime

import fastapi

import db


def search(state: str, district: str, mandal: str, from_time: datetime.datetime, to_time: datetime.datetime,
           resource_group_id: int):
    con = db.get_db()
    cur = con.cursor()
    print(state, district, mandal)
    cur.execute("SELECT * FROM resource WHERE state = ? AND district = ? AND mandal = ? AND resource_group_id = ?",
                (state, district, mandal, resource_group_id,))
    print(cur.fetchall())


def create(state: str, district: str, mandal: str, resource_group_id: int, data: str, owner: int):
    con = db.get_db()
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM resource WHERE state = ? AND district = ? AND mandal = ? AND resource_group_id = ? AND owner = ?",
        (state, district, mandal, resource_group_id, owner,))
    if len(cur.fetchall()):
        raise fastapi.HTTPException(status_code=409, detail="already exists")
    cur.execute("INSERT INTO resource (owner, state, district, mandal, data, resource_group_id) VALUES (?,?,?,?,?,?)",
                (owner, state, district, mandal, data, resource_group_id,))
    con.commit()


def order(resource_id: int, client: int, from_time: datetime.datetime, to_time: datetime.datetime, qty: float):
    con = db.get_db()
    cur = con.cursor()
    cur.execute("SELECT owner FROM resource WHERE resourceid = ?", (resource_id,))
    lessor = cur.fetchone()[0]
    cur.execute(
        "INSERT INTO orders(resourceid, lessor, lessee, start_time, end_time, quantity, order_status)\
         VALUES (?,?,?,?,?, ?, ?)",
        (resource_id, lessor, client, from_time, to_time, qty, 1,))
    con.commit()
