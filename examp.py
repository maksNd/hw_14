import sqlite3
import prettytable
from pprint import pp


query = """
            select title
            from netflix
            where release_year between 2009 and 2010
            limit 5
"""

with sqlite3.connect('./netflix.db') as connection:
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

print(result)
print()
for row in result:
    print(row)
