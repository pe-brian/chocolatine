import mysql.connector

from chocolatine import Request, lower


conn = mysql.connector.connect(
  host="localhost",
  user="sakila",
  password="p_ssW0rd",
  database="sakila",
  use_pure=True
)

cur = conn.cursor()
req = Request(compact=False, limit_to=5) \
        .table("actor")\
        .select("last_name", (lower("first_name") & " " & lower("last_name")).alias(">:name"))\
        .build()
print(req)
cur.execute(req)
print(cur.fetchall())
