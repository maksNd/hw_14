import sqlite3

from typing import List, Dict, Any


class DatabaseDAO:

    def _get_data_from_db_by_query(self, query: str) -> list:
        "Create connection and get data from db by query"
        with sqlite3.connect('./netflix.db') as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = []
            for row in cursor:
                result.append(row)
            return result

    def _get_formatted_result(self, *args, data_from_db):
        formatted_result = []
        for data in data_from_db:
            dict_for_append = {}
            for index, value in enumerate(args):
                dict_for_append[value] = data[index]
            formatted_result.append(dict_for_append)
        return formatted_result

    def search_for_title(self, title) -> list[dict[Any, Any]]:
        "Create query and get data from db by title"
        query = f"""
                    select title, country, release_year, listed_in, description
                    from netflix
                    where title = '{title}'
                    limit 1
        """
        data_from_db = self._get_data_from_db_by_query(query)
        result = self._get_formatted_result('title', 'country', 'release_year', 'genre', 'description',
                                            data_from_db=data_from_db)
        return result

    def search_by_years_range(self, year_1, year_2) -> list[dict[Any, Any]]:
        query = f"""
                    select title, release_year
                    from netflix
                    where release_year between {year_1} and {year_2}
                    limit 100
        """
        data_from_db = self._get_data_from_db_by_query(query)
        result = self._get_formatted_result('title', 'release_year', data_from_db=data_from_db)
        return result

    def _define_rating_query_part(self, rating_group):
        rating_group = rating_group.lower()
        if rating_group == 'children':
            return "rating like 'R'"
        if rating_group == 'family':
            return "rating like 'G' or rating like 'PG' or rating like 'PG-13'"
        if rating_group == 'adult':
            return "rating like 'R' or rating like 'NC-17'"
        return None

    def search_by_rating(self, rating_group: str) -> list[dict[Any, Any]]:
        rating_query = self._define_rating_query_part(rating_group)
        query = f"""
                    select title, rating, description
                    from netflix
                    where {rating_query}
                    limit 100
        """
        data_from_db = self._get_data_from_db_by_query(query)
        result = self._get_formatted_result('title', 'rating', 'description', data_from_db=data_from_db)
        return result

    def search_by_genre(self, genre):
        query = f"""
                    select title, description
                    from netflix
                    where listed_in like '%{genre}%'
                    limit 100
        """
        data_from_db = self._get_data_from_db_by_query(query)
        result = self._get_formatted_result('title', 'description', data_from_db=data_from_db)
        return result
