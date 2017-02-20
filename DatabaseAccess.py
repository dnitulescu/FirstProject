import sqlite3


def create_table():
    conn = sqlite3.connect("lite.db")  # creates or stablishes a connection
    cur = conn.cursor()  # pointer to acess the database
    cur = conn.execute("CREATE TABLE IF NOT EXISTS store (item TEXT, Quantity INTEGER , price REAL)")
    conn.commit()
    conn.close()


def insert_data(item, quantity, price):
    conn = sqlite3.connect("lite.db")  # creates or stablishes a connection
    cur = conn.cursor()  # pointer to acess the database
    cur.execute("INSERT INTO store VALUES(?,?,?)", (item, quantity, price))
    conn.commit()
    conn.close()


def view_db():
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM store")
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_db(item):
    conn = sqlite3.connect("lite.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM store WHERE item=?", (item,))
    conn.commit()
    conn.close()


def update_data(item, quantity, price):
    conn = sqlite3.connect("lite.db")  # creates or stablishes a connection
    cur = conn.cursor()  # pointer to acess the database
    cur.execute("UPDATE store SET quantity=?, price=? WHERE item=?", (quantity, price, item))
    conn.commit()
    conn.close()


delete_db("Water Glass")
update_data("Coffe Cup", 10, 10)
print(view_db())
