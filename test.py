from chocolatine import Request, Col


def test_request_001():

    assert Request(compact=True) \
        .table("payment") \
        .select(Col("staff_id").asc(), Col("amount").alias("total_amount").sum().desc()) \
        .group_by("staff_id") \
        .filter((Col("amount") > 0.99) & ~(Col("customer_id") == 3)) \
        .build() == \
        "SELECT staff_id, sum(amount) AS total_amount FROM payment WHERE ((amount > 0.99) AND NOT(customer_id = 3)) GROUP BY staff_id ORDER BY staff_id ASC, amount DESC"
