from database_dao import DatabaseDAO
from flask import Blueprint, jsonify

database_dao = DatabaseDAO()

bp_movie = Blueprint('bp_movie', __name__)


@bp_movie.route('/<title>')
def page_search_by_title(title):
    return jsonify(database_dao.search_for_title(title))


@bp_movie.route('/<int:year_1>/to/<int:year_2>')
def page_search_by_year(year_1, year_2):
    return jsonify(database_dao.search_by_years_range(year_1, year_2))


@bp_movie.route('/rating/<rating_group>')
def page_search_by_rating_group(rating_group):
    return jsonify(database_dao.search_by_rating(rating_group))


@bp_movie.route('/genre/<genre>')
def page_search_by_genre(genre):
    return jsonify(database_dao.search_by_genre(genre))


@bp_movie.route('/type_year_genre/<type>/<int:year>/<genre>')
def page_by_type_year_genre(type, year, genre):
    return jsonify(database_dao.search_by_type_release_year_genre(type, year, genre))