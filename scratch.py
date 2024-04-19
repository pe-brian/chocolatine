from chocolatine import Query


req = Query(compact=True).table("actor").select("first_name", "last_name")
print(req)
