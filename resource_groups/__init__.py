import typing

import db
import mytypes


def list_groups() -> typing.List[mytypes.ResourceGroupInfo]:
    con = db.get_db()
    cur = con.cursor()
    cur.execute("SELECT resourceid, name, unit FROM resource_group")
    rows = cur.fetchall()
    rv = []
    for row in rows:
        rv.append(mytypes.ResourceGroupInfo(id=row[0], name=row[1], unit=row[2]))
    return rv
