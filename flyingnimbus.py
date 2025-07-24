import psycopg2 as pg2
import os
import csv
from dotenv import load_dotenv

load_dotenv()

# connection with postgres
def get_connection():
    try:
        conn = pg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn, conn.cursor()
    except Exception as e:
        print(f"Error: {e}")

table_list = ["actor", "film", "film_actor", "category", "film_category", "store", "inventory", "rental", "payment", "staff",
              "customer", "address", "city", "country"]

def your_query(query: str, cur, conn, filename: str = None) -> tuple:
    your_query.calls += 1
    print(f"\n Query result {your_query.calls}:\n")

    try:
        cur.execute(query)
        rows = cur.fetchall()

        # schema
        columns = [desc[0] for desc in cur.description] 
        print(columns)

        # this loop is for the tables not the calls!
        for item in rows:
            print(item)

        if filename:
            with open(filename,"w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(columns) # for schema
                writer.writerows(rows) # data
            print(f"\nData exported to {filename}\n")
        
        return rows, columns


    except Exception as e:
        print(f"random error: {e}")


your_query.calls = 0

if __name__ == "__main__":

     # tuple unpacks the shit
    conn, cur = get_connection()

    # Top 5 customers by Total Payment
    your_query("""SELECT cust.customer_id, cust.first_name, cust.last_name, SUM(pay.amount) AS total_paid
                FROM customer cust
                JOIN payment pay ON cust.customer_id = pay.customer_id
                GROUP BY cust.customer_id, cust.first_name, cust.last_name
                ORDER BY total_paid DESC
                LIMIT 5""", cur, conn, "top5.csv")

    # Customers who have rented films in the 'Action' category
    your_query("""SELECT DISTINCT c.customer_id, c.first_name, c.last_name
                FROM customer c
                JOIN rental r ON c.customer_id = r.customer_id
                JOIN inventory i ON r.inventory_id = i.inventory_id
                JOIN film_category fc ON i.film_id = fc.film_id
                JOIN category cat ON fc.category_id = cat.category_id
                WHERE cat.name = 'Action'
                LIMIT 5        
    """, cur, conn,"action.csv")

    # Customers who never made a payment
    your_query("""SELECT c.customer_id, c.first_name, c.last_name
    FROM customer c
    LEFT JOIN payment p ON c.customer_id = p.customer_id
    WHERE p.payment_id IS NULL
    LIMIT 5
    """, cur, conn,"nopayment.csv")

    # Movies that were never rented
    your_query("""SELECT f.film_id, f.title
    FROM film f
    LEFT JOIN inventory i ON f.film_id = i.film_id
    LEFT JOIN rental r ON i.inventory_id = r.inventory_id
    WHERE r.rental_id IS NULL
    LIMIT 5
    """, cur, conn,"norent.csv")

    # Label customers based on how much money they have spent
    your_query("""SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        COALESCE(SUM(p.amount), 0) AS total_paid,
        
        CASE 
            WHEN COALESCE(SUM(p.amount), 0) >= 100 THEN 'High $$$'
            WHEN COALESCE(SUM(p.amount), 0) BETWEEN 50 AND 99.99 THEN 'Medium $$'
            WHEN COALESCE(SUM(p.amount), 0) BETWEEN 1 AND 49.99 THEN 'Low $'
            ELSE 'No Payment'
        END AS spending_tier

    FROM customer c
    LEFT JOIN payment p ON c.customer_id = p.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
    ORDER BY total_paid DESC
    LIMIT 5
    """, cur, conn,"spending_tiers.csv")

    cur.close()
    conn.close()










# hellll yeahh prod worthy babyyy
