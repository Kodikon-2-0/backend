import datetime

import fastapi

import db
import mytypes


def search(state: str, district: str, mandal: str, from_time: datetime.datetime, to_time: datetime.datetime,
           resource_group_id: int):
    con = db.get_db()
    cur = con.cursor()
    print(state, district, mandal, from_time, to_time)
    cur.execute(
        "SELECT resource.*, availability.start_time, availability.end_time FROM \
        resource JOIN availability ON\
         availability.resource_id = resource.resourceid \
         WHERE availability.start_time < ? AND availability.end_time > ? \
          AND state = ? AND district = ? AND mandal = ? AND resource_group_id = ?",
        (from_time, to_time, state, district, mandal, resource_group_id,))
    rv = []
    for row in cur.fetchall():
        rv.append(mytypes.SearchResultsInfo(resource_id=row[0], owner=row[1], state=row[2], district=row[3], mandal=row[4],
                                            data=row[5], available_from=row[7], available_till=row[8]))
    return rv


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


def set_available_range(resource_id: int, start: datetime.datetime, end: datetime.datetime, user_id: int):
    con = db.get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM resource WHERE resourceid = ? AND owner = ?", (resource_id, user_id,))
    if not len(cur.fetchall()):
        raise fastapi.HTTPException(status_code=404, detail="not found")
    cur.execute("INSERT INTO availability(resource_id, start_time, end_time) VALUES (?,?,?)",
                (resource_id, start, end,))
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
