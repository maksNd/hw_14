import sqlite3
from constants import DATABASE

from typing import List, Dict, AnyStr


class DatabaseDAO:

    def __init__(self, sourse: str = DATABASE):
        self.sourse = sourse

    def _get_data_from_db_by_query(self, query: str) -> List[Dict]:
        """Create connection and get data from db by query"""
        with sqlite3.connect(self.sourse) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result

    def _get_formatted_result(self, *args, data_from_db) -> List[Dict]:
        """Revert data to needed format"""
        formatted_result = []
        for data in data_from_db:
            dict_for_append = {}
            for index, value in enumerate(args):
                dict_for_append[value] = data[index]
            formatted_result.append(dict_for_append)
        return formatted_result

    def search_for_title(self, title) -> List[Dict[AnyStr, AnyStr]]:
        """Create query and get data from db by title"""
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

    def search_by_years_range(self, year_1, year_2) -> List[Dict[AnyStr, AnyStr]]:
        """Create query and get data from db by years rane"""
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
        """Change rating group by keyword"""
        rating_group = rating_group.lower()
        if rating_group == 'children':
            return "rating like 'R'"
        if rating_group == 'family':
            return "rating like 'G' or rating like 'PG' or rating like 'PG-13'"
        if rating_group == 'adult':
            return "rating like 'R' or rating like 'NC-17'"
        return None

    def search_by_rating(self, rating_group: str) -> List[Dict[AnyStr, AnyStr]]:
        """Create query and get data from db by rating"""
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

    def search_by_genre(self, genre: str) -> List[Dict[AnyStr, AnyStr]]:
        """Create query and get data from db by genre"""
        query = f"""
                    select title, description
                    from netflix
                    where  listed_in
                    like '%{genre}%'
        """

        data_from_db = self._get_data_from_db_by_query(query)
        result = self._get_formatted_result('title', 'description', data_from_db=data_from_db)
        return result

    def search_by_type_release_year_genre(self, type, release_year, genre):
        """Create query and get data from db by type, release year, genre"""
        query = f"""
                    select type, description
                    from netflix
                    where type like '%{type}%'
                    and release_year = {release_year}
                    and listed_in like '%{genre}%'
                    limit 100
        """
        data_from_db = self._get_data_from_db_by_query(query)
        result = self._get_formatted_result('title', 'description', data_from_db=data_from_db)
        return result

    def search_actors_wierd_foo(self, actor_1, actor_2):
        """
        Функция, которая получает в качестве аргумента имена двух актеров,
        сохраняет всех актеров из колонки cast и возвращает список тех, кто играет с ними в паре больше 2 раз
        """

        query = f"""
                    select netflix.cast
                    from netflix
                    where netflix.cast like '%{actor_1}%' and netflix.cast like '%{actor_2}%'
        """
        data_from_db = self._get_data_from_db_by_query(query)

        # Находим всех актеров, которые одновременно играли в паре с actor_1 и actor_2
        for group in data_from_db:
            all_persons = set()
            for person in group[0].split(', '):
                if person not in (actor_1, actor_2):
                    all_persons.add(person)

        # Находим актеров, которые одновременно играли в паре с actor_1 и actor_2 более 2х раз
        finded_person = []
        for person in all_persons:
            counter = 0
            for group in data_from_db:
                if person in group[0].split(', '):
                    counter += 1
            if counter > 2:
                finded_person.append(person)

        return finded_person

# db_dao = DatabaseDAO()
# print(db_dao.search_actors_wierd_foo('Jack Black', 'Dustin Hoffman'))
