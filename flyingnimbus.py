import psycopg2 as pg2
import os

# connection with postgres
conn = pg2.connect(database='dvdrental', user='postgres',password='satu')
cur = conn.cursor()
table_list = ["actor", "film", "film_actor", "category", "film_category", "store", "inventory", "rental", "payment", "staff",
              "customer", "address", "city", "country"]

def your_query(query: str) -> str:
    try:
        cur.execute(query)
        rows = cur.fetchall()

        # schema
        columns = [desc[0] for desc in cur.description] 
        print(columns)
        for item in rows:
            print(item)

        cur.close()
        conn.close()
    except Exception as e:
        print("random error")

your_query("""SELECT cust.customer_id, cust.first_name, cust.last_name, SUM(pay.amount) AS total_paid
              FROM customer cust
              JOIN payment pay ON cust.customer_id = pay.customer_id
              GROUP BY cust.customer_id, cust.first_name, cust.last_name
              ORDER BY total_paid DESC
              LIMIT 5""")
