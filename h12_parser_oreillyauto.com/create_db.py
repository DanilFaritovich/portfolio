import sqlite3

conn = sqlite3.connect('items.db')
cur = conn.cursor()

def create_item_db():
    cur.execute("""
                CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                year TEXT,
                make TEXT,
                model TEXT,
                sub_model TEXT,
                engine TEXT,
                category TEXT,
                supplier TEXT,
                location TEXT,
                part_number TEXT,
                image_url TEXT,
                title TEXT,
                description TEXT,
                story TEXT);
                """)
    conn.commit()


def ckeck_last_car():
    cur.execute("""
                SELECT year, make, model, sub_model, engine, story
                FROM items
                ORDER BY id DESC
                LIMIT 1
                """)
    return cur.fetchone()

def insert_item(id, year, make, model, sub_model, engine, category, supplier, location, part_number, image_url, title, description, story):
    if '\'' in str(category):
        category = category.replace('\'', '\'\'')
    if '\'' in str(supplier):
        supplier = supplier.replace('\'', '\'\'')
    if '\'' in str(location):
        location = location.replace('\'', '\'\'')
    if '\'' in str(part_number):
        part_number = part_number.replace('\'', '\'\'')
    if '\'' in str(title):
        title = title.replace('\'', '\'\'')
    if '\'' in str(description):
        description = description.replace('\'', '\'\'')
    cur.execute(f"""
                SELECT id
                FROM items
                WHERE year = '{year}' and make = '{make}' and model = '{model}' and sub_model = '{sub_model}' 
                and engine = '{engine}' and category = '{category}' and supplier = '{supplier}'
                and location = '{location}' and part_number = '{part_number}' and image_url = '{image_url}'
                and title = '{title}' and description = '{description}' and story = '{story}';
                """)
    if cur.fetchone() is None:
        cur.execute(f"""
                    INSERT INTO items(id, year, make, model, sub_model, engine, category, supplier, location, 
                    part_number, image_url, title, description, story)
                    VALUES ({id}, '{year}', '{make}', '{model}', '{sub_model}', '{engine}', '{category}', '{supplier}'
                    , '{location}', '{part_number}', '{image_url}', '{title}', '{description}', '{story}');
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