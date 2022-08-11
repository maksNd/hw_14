from flask import Flask, jsonify
from bp_movie import bp_movie

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(bp_movie, url_prefix='/movie/')

if __name__ == '__main__':
    app.run()
