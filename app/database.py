from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# import psycopg
# from psycopg.rows import dict_row

from config import settings

engine = create_engine(settings.DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg.connect(
#         host=settings.DB_HOST,
#         dbname=settings.DB_NAME,
#         user=settings.DB_USER,
#         password=settings.DB_PASS,
#         row_factory=dict_row,
#     )
#     cursor = conn.cursor()
#     print("Database connection was succesfull!")
# except Exception as error:
#     print("Connection to database failed: ", error)
