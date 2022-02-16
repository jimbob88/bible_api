import mysql.connector
from fastapi import FastAPI, Depends, Query
from typing import Optional, List
import os
from database import *

user = os.environ["SQL_USER"]
# passwd = os.environ["SQL_PASSWORD"]
passwd = ""

description = """
The Bible API was designed to help you grab information from the bible quickly and efficiently

Currently this software can:
 - Say **Hello World**
 - Make requests for extracts of the bible
"""

app = FastAPI(title="BibleAPI", version="0.0.1")


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


@app.get("/get_bibles/")
async def get_bibles(curs=Depends(get_cursor)):
    curs.execute("show tables;")
    return {"status": "OK", "bibles": [r[0] for r in curs]}


@app.get("/text_query/")
async def read_item(
    bible_name: List[str] = Query(["deu1912_vpl"]),
    book: Optional[List[str]] = Query(None),
    chapter: Optional[List[int]] = Query(None),
    verseID: Optional[List[str]] = Query(None),
    canon_order: Optional[List[str]] = Query(None),
    startVerse: Optional[List[int]] = Query(None),
    endVerse: Optional[List[int]] = Query(None),
    verseContains: Optional[List[str]] = Query(None),
    curs=Depends(get_cursor),
):
    where_clauses = []
    if book:
        temp_str = "("
        temp_str += f'book = "{book[0]}"'
        for b in book[1:]:
            temp_str += f' OR book = "{b}"'
        temp_str += ")"
        where_clauses.append(temp_str)
    if chapter:
        temp_str = f'(chapter = "{chapter[0]}"'
        for c in chapter[1:]:
            temp_str += f' OR chapter = "{c}"'
        temp_str += ")"
        where_clauses.append(temp_str)
    if verseID:
        temp_str = f'(verseID = "{verseID[0]}"'
        for v in verseID[1:]:
            temp_str += f' OR verseID = "{v}"'
        temp_str += ")"
        where_clauses.append(temp_str)
    if canon_order:
        temp_str = f'(canon_order = "{canon_order[0]}"'
        for c in canon_order[1:]:
            temp_str += f' OR canon_order = "{c}"'
        temp_str += ")"
        where_clauses.append(temp_str)
    if startVerse:
        temp_str = f'(startVerse = "{startVerse[0]}"'
        for s in startVerse[1:]:
            temp_str += f' OR startVerse = "{s}"'
        temp_str += ")"
        where_clauses.append(temp_str)
    if endVerse:
        temp_str = f'(endVerse = "{endVerse[0]}"'
        for e in endVerse[1:]:
            temp_str += f' OR endVerse = "{e}"'
        temp_str += ")"
        where_clauses.append(temp_str)

    if verseContains:
        for match in verseContains:
            where_clauses.append(f"verseText LIKE '%{match}%'")

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
