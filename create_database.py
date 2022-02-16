import scandir_rs as scandir
from prompt_toolkit import prompt
import os
import re
import mysql.connector
import unicodedata
import tqdm

user = prompt("User: ")
passwd = prompt("Password: ", is_password=True)

cnx = mysql.connector.connect(
    user=user,
    password=passwd,
    host="127.0.0.1",
    database="bible_api",
    charset="utf8mb4",
    use_unicode=True,
)
cursor = cnx.cursor()

for root, dirs, files in scandir.walk.Walk("./sources"):
    for file in files:
        with open(os.path.join(root, file), "r", encoding="utf8") as f:
            database_name = file.replace(".sql", "")
            print(database_name)
            sql = f.read()
            sql = sql.replace("USE sofia;", "")
            if re.match(r"(DROP TABLE IF EXISTS )sofia.(" + database_name + ");", sql):
                sql = re.sub(
                    r"(DROP TABLE IF EXISTS )sofia.(" + database_name + r");",
                    "\g<1>bible_api.\g<2>;",
                    sql,
                )
            else:
                sql = f"DROP TABLE IF EXISTS bible_api.{database_name};\n" + sql
            # print(sql)

            sql = sql.replace(" ENGINE=MyISAM", "")
            sql = sql.replace(f"LOCK TABLES {database_name} WRITE;", "")
            sql = sql.replace("UNLOCK TABLES;", "")
            sql = (
                unicodedata.normalize("NFKD", sql)
                .encode("ascii", "ignore")
                .decode("utf8")
            )
            for command in tqdm.tqdm(sql.split(";\n")):
                if not re.match(r"^\s*$", command) and command != "":
                    cursor.execute(command)

cnx.commit()
cursor.close()
cnx.close()
