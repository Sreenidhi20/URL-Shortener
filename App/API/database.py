import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

SERVER_NAME = os.getenv("SERVER_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")


def get_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER_NAME};"
        f"DATABASE={DATABASE_NAME};"
        f"Trusted_Connection=yes;"
    )

    try:
        return pyodbc.connect(connection_string)
    except Exception as e:
        print(e)
        return None