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
req = Request().table("film:f")\
               .select("f.title", _("a.first_name") & " " & _("a.last_name"))\
               .join("film_actor:fa", _("fa.film_id") == _("f.film_id"))\
               .join("actor:a", _("a.actor_id") == _("fa.actor_id"))\
               .build()
print(req)
cur.execute(req)
print(cur.fetchone())
