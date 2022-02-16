from matplotlib.pyplot import connect
import mysql.connector
from fastapi import FastAPI
from typing import Optional
import os


user = os.environ["SQL_USER"]
# passwd = os.environ["SQL_PASSWORD"]
passwd = ""


cnx = mysql.connector.connect(
    user=user,
    password=passwd,
    host="127.0.0.1",
    database="bible_api",
    charset="utf8mb4",
    use_unicode=True,
)
cursor = cnx.cursor()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/bible_query/{bible_name}")
async def read_item(
    bible_name: str, book: Optional[str] = None, chapter: Optional[int] = None
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

    cursor.execute(sql)

    return {"bible_name": bible_name, "sql": sql}


cursor.close()
cnx.close()
