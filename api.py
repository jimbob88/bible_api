import mysql.connector
from fastapi import FastAPI
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


cursor.close()
cnx.close()
