import mysql.connector

from chocolatine import Request, Col as _, lower


conn = mysql.connector.connect(
  host="localhost",
  user="sakila",
  password="p_ssW0rd",
  database="sakila",
  use_pure=True
)

cur = conn.cursor()
req = Request(compact=False) \
        .table("actor")\
        .select("last_name", (lower("first_name") & " " & lower("last_name")).alias(">:name"))\
        .filter(_("last_name") << ("JANE", "LUC"))\
        .build()
print(req)
cur.execute(req)
print(cur.fetchone())
