import mysql.connector

from chocolatine.col import Col
from chocolatine.request import Request
from chocolatine.shortcut import count


conn = mysql.connector.connect(
  host="localhost",
  user="sakila",
  password="p_ssW0rd",
  database="sakila",
  use_pure=True
)

"""
#   SELECT last_name, COUNT(*) AS 'count' 
#   FROM actor 
#   GROUP BY last_name 
#   HAVING COUNT(*) > 1;
"""

cur = conn.cursor()
req = Request().table("actor").select("last_name", count().alias("count")).group_by("last_name").filter(count() > 1).filter(Col("last_name").like("BE%")).build()
print(req)
cur.execute(req)
print(cur.fetchall())
