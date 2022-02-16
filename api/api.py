import mysql.connector
from fastapi import FastAPI, Depends
from typing import Optional
import os
from database import *

user = os.environ["SQL_USER"]
# passwd = os.environ["SQL_PASSWORD"]
passwd = ""


app = FastAPI()


def get_cursor():
    db = None
    db = cnx.cursor()
    yield db


@app.on_event("startup")
async def startup():
    if cnx.is_closed():
        cnx.connect()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/text_query/{bible_name}")
async def read_item(
    bible_name: str,
    book: Optional[str] = None,
    chapter: Optional[int] = None,
    curs=Depends(get_cursor),
):
    sql = f"SELECT * FROM {bible_name}"
    where_clauses = []
    if book:
        where_clauses.append(f'book = "{book}"')
    if chapter:
        where_clauses.append(f"chapter = {chapter}")

    if len(where_clauses) >= 1:
        sql += f" WHERE "
        sql += where_clauses[0]
        for clause in where_clauses[1:]:
            sql += f" AND {clause}"
        sql += ";"

    curs.execute(sql)
    headers = [i[0] for i in curs.description]
    r = [dict(zip(headers, result)) for result in curs]
    return {"bible_name": bible_name, "sql": sql, "r": r}


cursor.close()
cnx.close()
