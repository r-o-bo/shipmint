import psycopg2 as pg2
import os

# connection with postgres
conn = pg2.connect(database='dvdrental', user='postgres',password='satu')
cur = conn.cursor()

def your_query(query):
    try:
        cur.execute()
        rows = cur.fetchall()

        # schema
        columns = [desc[0] for desc in cur.description]

        print(f"Table: {(query.split()[-1])}")
        print(columns)
        for item in rows:
            print(item)

        cur.close()
        conn.close()
    except Exception as e:
        print("random error")