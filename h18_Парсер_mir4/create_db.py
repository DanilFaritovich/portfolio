import sqlite3

conn = sqlite3.connect('items.db')
cur = conn.cursor()

def create_item_db():
    cur.execute("""
                CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                url TEXT,
                name TEXT,
                price TEXT,
                lvl TEXT);
                """)
    conn.commit()


def ckeck_last_car():
    cur.execute("""
                SELECT year, make, model, sub_model, engine
                FROM items
                ORDER BY id DESC
                LIMIT 1
                """)
    return cur.fetchone()

def insert_item(id, url, name, price, lvl):
    cur.execute(f"""
                SELECT id, url, name, price, lvl
                FROM items
                WHERE name = '{name}' and price = '{price}' and lvl = '{lvl}';
                """)
    if cur.fetchone() is None:
        cur.execute(f"""
                    INSERT INTO items(id, url, name, price, lvl)
                    VALUES ({id}, '{url}', '{name}', '{price}', '{lvl}');
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