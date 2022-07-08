import sqlite3

conn = sqlite3.connect('items.db')
cur = conn.cursor()

def create_db():
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS items(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    time DATETIME,
                    price FLOAT,
                    wheather TEXT,
                    wind_power FLOAT,
                    wind_direction TEXT,
                    temperature FLOAT);
                    """)
    conn.commit()

def insert_item(id, time, price, wheather, wind_power, wind_direction, temperature):
    cur.execute(f"""
                SELECT id, time, price, wheather, wind_power, wind_direction, temperature
                FROM items
                WHERE time = '{time}';
                """)
    if cur.fetchone() is None:
        cur.execute(f"""
                    INSERT INTO items(id, time, price, wheather, wind_power, wind_direction, temperature)
                    VALUES ({id}, '{time}', '{price}', '{wheather}', '{wind_power}', 
                    '{wind_direction}', '{temperature}');
                    """)
        conn.commit()

def create_id():
    item = cur.execute("""
                SELECT id
                FROM items
                ORDER BY id DESC
                LIMIT 1
                """).fetchone()
    if item is not None:
        return item[0] + 1
    else:
        return 0