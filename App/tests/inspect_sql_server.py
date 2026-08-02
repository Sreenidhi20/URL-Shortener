import os
import pyodbc

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('SERVER_NAME')};DATABASE={os.getenv('DATABASE_NAME')};Trusted_Connection=yes;"
)
cur = conn.cursor()
cur.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('Registry','HealthCheck') ORDER BY TABLE_SCHEMA, TABLE_NAME")
print(cur.fetchall())

for query in ["SELECT COUNT(*) FROM dbo.Registry", "SELECT COUNT(*) FROM URL.Registry"]:
    try:
        cur.execute(query)
        print(query, '=>', cur.fetchone()[0])
    except Exception as exc:
        print(query, 'ERROR', exc)

conn.close()
