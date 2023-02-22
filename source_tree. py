import sqlite3

def find_source_tree(primary_key, db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Execute SQL query to find foreign keys pointing to the primary key
    c.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    for table in tables:
        c.execute("PRAGMA foreign_key_list({})".format(table[1]))
        foreign_keys = c.fetchall()
        for foreign_key in foreign_keys:
            if foreign_key[3] == primary_key:
                print("Table '{}' has a foreign key referencing the primary key in table '{}', column '{}'".format(table[1], foreign_key[2], foreign_key[3]))
                find_source_tree(foreign_key[3], db_path) # Recursively search for foreign keys referencing this key

    conn.close()
