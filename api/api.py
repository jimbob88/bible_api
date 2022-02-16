import mysql.connector
from fastapi import FastAPI, Depends, Query
from typing import Optional, List
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


@app.get("/text_query/")
async def read_item(
    # bible_name: List[str] = Query(None),
    bible_name: List[str] = Query(["deu1912_vpl"]),
    book: Optional[str] = None,
    chapter: Optional[int] = None,
    verseID: Optional[str] = None,
    canon_order: Optional[str] = None,
    startVerse: Optional[int] = None,
    endVerse: Optional[int] = None,
    curs=Depends(get_cursor),
):
    where_clauses = []
    if book:
        where_clauses.append(f'book = "{book}"')
    if chapter:
        where_clauses.append(f"chapter = {chapter}")
    if verseID:
        where_clauses.append(f'verseID = "{verseID}"')
    if canon_order:
        where_clauses.append(f'canon_order = "{canon_order}"')
    if startVerse:
        where_clauses.append(f"startVerse = {startVerse}")
    if endVerse:
        where_clauses.append(f"endVerse = {endVerse}")

    if len(where_clauses) >= 1:
        where_clause = f" WHERE "
        where_clause += where_clauses[0]
        for clause in where_clauses[1:]:
            where_clause += f" AND {clause}"

    queries = [
        f"SELECT *, '{bible}' AS bible_name FROM {bible}" + where_clause
        for bible in bible_name
    ]
    sql = "\nUNION\n".join(queries)
    print(sql)
    curs.execute(sql)
    headers = [i[0] for i in curs.description]
    r = [dict(zip(headers, result)) for result in curs]
    return {"status": "OK", "bible_name": bible_name, "sql": sql, "r": r}


cursor.close()
cnx.close()
