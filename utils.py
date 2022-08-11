import sqlite3


def get_data_from_db_by_query(query: str) -> list:
    "Create connection and get data from db by query"
    with sqlite3.connect('./netflix.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def search_for_title(title) -> dict:
    "Create query and get data from db by title"
    query = f"""
                select title, country, release_year, listed_in, description
                from netflix
                where title = '{title}'
                limit 1
    """
    data_from_db = get_data_from_db_by_query(query)[0]
    return {
        "title": data_from_db[0],
        "country": data_from_db[1],
        "release_year": data_from_db[2],
        "genre": data_from_db[3],
        "description": data_from_db[4]}


def search_by_years_range(year_1, year_2) -> list:
    query = f"""
                select title, release_year
                from netflix
                where release_year between {year_1} and {year_2}
                limit 100
    """
    data_from_db = get_data_from_db_by_query(query)
    return data_from_db



def search_by_rating():
    ...


from pprint import pp

print(search_by_years_range(2010, 2020))
# print(type(search_for_title('A Yellow Bird')))
