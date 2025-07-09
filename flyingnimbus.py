import psycopg2 as pg2
import os

print("hello world")

# connection with postgres
conn = pg2.connect(database='dvdrental', user='postgres',password='satu')


cur = conn.cursor()
cur.execute("SELECT * FROM payment")
rows = cur.fetchmany(10)

# schema
columns = [desc[0] for desc in cur.description]
print(columns)
for item in rows:
    print(item)

cur.close()
conn.close()