import sqlite3
from pprint import pp


def get_data_from_db_by_query(query: str) -> list:
    "Create connection and get data from db by query"
    with sqlite3.connect('data/netflix.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row)

        return result


def get_formatted_result(*args, data_from_db):
    formatted_result = []
    for data in data_from_db:
        dict_for_append = {}
        for index, value in enumerate(args):
            dict_for_append[value] = data[index]
        formatted_result.append(dict_for_append)
    return formatted_result


def exam_search_by_title(title):
    query = f"""
                select title, country, release_year, listed_in, description
                from netflix
                where title = '{title}'
                limit 1
    """
    data_from_db = get_data_from_db_by_query(query)
    result = get_formatted_result('title', 'country', 'release_year', 'genre', 'description', data_from_db=data_from_db)
    return result


# pp(exam_search_by_title('Al Hayba'))
# pp(len(exam_search_by_title('Al Hayba')))