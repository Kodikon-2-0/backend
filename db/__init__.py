import sqlite3

database = None


def get_db():
    global database
    if database is None:
        database = sqlite3.connect("./db.db")
    return database
