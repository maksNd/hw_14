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
    result = []
    for data in data_from_db:
        result.append({
            'title': data[0].replace('\u200b', ''),
            'release_year': data[1]
        })
    return result


def search_by_rating(rating_group: str):
    rating_group = rating_group.lower()
    if rating_group == 'children':
        rating_query = "rating like 'R'"
    if rating_group == 'family':
        rating_query = "rating like 'G' or rating like 'PG' or rating like 'PG-13'"
    if rating_group == 'adult':
        # rating_query = "('R', 'NC-17')"
        rating_query = "rating like 'R' or rating like 'NC-17'"

    query = f"""
                select title, rating, description
                from netflix
                where {rating_query}
                limit 100
    """
    data_from_db = get_data_from_db_by_query(query)
    return data_from_db


# from pprint import pp
# pp(search_by_rating('adult'))
# print(type(search_for_title('A Yellow Bird')))
