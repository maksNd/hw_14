import sqlite3
from pprint import pp


query = """
            select distinct type
            from netflix
            
"""

with sqlite3.connect('data/netflix.db') as connection:
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

print(result)
print()
for row in result:
    print(row)
