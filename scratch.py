import mysql.connector

from chocolatine import Request, month, year, sum


conn = mysql.connector.connect(
  host="localhost",
  user="sakila",
  password="p_ssW0rd",
  database="sakila",
  use_pure=True
)

cur = conn.cursor()
req = Request(compact=False)\
        .table("staff:s")\
        .select("s.first_name", "s.last_name", sum("p.amount"))\
        .join("payment:p", "staff_id")\
        .filter((month("p.payment_date") == 8) & (year("p.payment_date") == 2005))\
        .group_by("s.staff_id")\
        .build()
print(req)
cur.execute(req)

print(cur.fetchall())
