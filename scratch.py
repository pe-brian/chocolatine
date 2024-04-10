import mysql.connector

from chocolatine.col import Col as _
from chocolatine.request import Request


conn = mysql.connector.connect(
  host="localhost",
  user="sakila",
  password="p_ssW0rd",
  database="sakila",
  use_pure=True
)

cur = conn.cursor()
req = Request(compact=False).table("film")\
               .select("title", "film_id", _("first_name") & " " & _("last_name"))\
               .join("film_actor", "film_id")\
               .join("actor", "actor_id")\
               .build()
print(req)
cur.execute(req)
print(cur.fetchone())
