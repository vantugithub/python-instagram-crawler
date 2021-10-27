from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import Utils
import mysql_query
from Utils import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

store = [
    {
        "name": "L298N",
        "brand": "Nshop",
        "available": 20,
        "price": "40.000"
    },
    {
        "name": "Arduino Uno",
        "brand": "Hshop",
        "available": 16,
        "price": "90.000"
    }
]


@app.route('/')
def hello():
    return {'hello': 'Thế Giới'}


def updateData():
    try:
        session = Utils.instaLogin()
        if session.context.is_logged_in:
            mysql_query.resetDataAndUpdateDataPerWeek()
            list_of_hashtag = Utils.fetchPostsData(session, str('netflix'), 30)
            list_of_hashtag_final = Utils.get_hashtag_final(list_of_hashtag)
            mysql_query.insertUserAndPost(list_of_hashtag_final)
            print("Update Success")
    except:
        print("Update Data Failed")


@app.route('/store')
def get_store():
    return jsonify(store)


@app.route('/store/<int:index>')
def get_product(index):
    product = store[index]
    return jsonify(product)


@app.route('/store', methods=['POST'])
def add_product():
    product = request.get_json()
    store.append(product)
    return {'id': len(store)}, 200


@app.route('/ins/gethashtag/<string:hashtag>')
def get_status_login_ins(hashtag):
    # list_of_hashtag = Utils.login_ins(str(hashtag), 200)
    # list_of_hashtag_final = Utils.get_hashtag_final(list_of_hashtag)
    # mysql_query.insertUserAndPost(list_of_hashtag_final)
    list_of_hashtag_final = Utils.wordCountDict(hashtag)
    return json.dumps(list_of_hashtag_final)


scheduler = BackgroundScheduler()
scheduler.add_job(func=updateData, trigger="interval", seconds=604800)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
