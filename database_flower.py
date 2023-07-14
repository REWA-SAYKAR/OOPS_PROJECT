import sqlite3

#creating the database connector
conn = sqlite3.connect('flower.db')
#creating the cursor
cursor = conn.cursor()

#creating the table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS flower(
        id INTEGER PRIMARY KEY,
        flower_name TEXT,
        price INTEGER,
        quantity INTEGER)''')

flowers = [
    ('Anemones',265,10),
    ('White Roses',300,10),
    ('Tulips',280,10)
]

for flower in flowers:
    cursor.execute('INSERT INTO flower (flower_name,price,quantity) VALUES (?,?,?)',flower)

#commiting the changes
conn.commit()
#closing the connection
conn.close()

