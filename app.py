from flask import Flask, jsonify
from utils import search_for_title, search_by_years_range, search_by_rating

app = Flask(__name__)
app.json.ensure_ascii = False


@app.route('/movie/<title>')
def page_search_by_title(title):
    return jsonify(search_for_title(title))


@app.route('/movie/<int:year_1>/to/<int:year_2>')
def page_search_by_year(year_1, year_2):
    return jsonify(search_by_years_range(year_1, year_2))


@app.route('/movie_by_rating/<rating_group>')
def page_search_by_rating_group(rating_group):
    return search_by_rating(rating_group)


if __name__ == '__main__':
    app.run()
