from flask import Flask, jsonify, abort, make_response, request
from util import token
from ElasticsearchApiDAO import getAdsList, insert_ads_2_db

app = Flask(__name__)

@app.route('/newAds', methods=['POST'])
def new_ads():
    if not request.json or not 'title' or not 'price' or not 'image' in request.json:
        abort(400)
    ads = {
        'title': request.json['title'],
        'price': request.json['price'],
        'image': request.json['image'],
        'description': request.json.get('description', ""),
    }
    insert_ads_2_db(ads)
    return jsonify(ads)

@app.route('/getAds', methods=['POST'])
def get_ads():
    if not request.json or not 'paper' in request.json:
        abort(400)
    paper = request.json['paper']
    adsList = getAdsList(token(paper))
    return jsonify(adsList)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Truyen thieu gia tri'}), 400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
