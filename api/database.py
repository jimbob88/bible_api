# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{os.environ['SQL_USER']}@localhost:3306/bible_api"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
import mysql.connector
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
