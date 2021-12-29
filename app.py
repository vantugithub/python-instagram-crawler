import psycopg2
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS

import Utils
import config
import mysql_query
from Utils import *

app = Flask(__name__)
CORS(app)
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
        connection = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
                                      host=config.mysql_host)
        session = Utils.instaLogin()
        if session.context.is_logged_in:
            # mysql_query.resetDataAndUpdateDataPerWeek()
            # list_of_hashtag = Utils.fetchPostsData(session, str('netflix'), 30)
            # list_of_hashtag_final = Utils.get_hashtag_final(list_of_hashtag)
            # mysql_query.insertUserAndPost(list_of_hashtag_final)
            date = 0
            if mysql_query.checkDateExist(connection) == 0:
                mysql_query.insertDate(connection)
                date += mysql_query.checkDateExist(connection)
            else:
                date += mysql_query.checkDateExist(connection)
            list_topic = mysql_query.getTopicActiveTrue(connection)
            for i in list_topic:
                list_of_hashtag = Utils.fetchPostsData(session, str(i[2]), 50)
                list_of_hashtag_final = Utils.get_hashtag_final(list_of_hashtag)
                mysql_query.insertUserAndPost(list_of_hashtag_final, str(i[2]))
                number = []
                for k in range(0, len(list_of_hashtag_final)):
                    temp = list_of_hashtag_final[k]['caption'].split()
                    for j in temp:
                        try:
                            # if checkLanguage(str(j)) is True and str(hashtag).lower() not in j.lower():
                            number.append(j)
                        except:
                            continue
                word_could_dict = Counter(number)
                ok = list(reversed(sorted(word_could_dict.items(), key=lambda item: item[1])))
                print(ok)
                mysql_query.UpdateAnalysis(ok, date, int(mysql_query.getIdTopic(connection, i[2])))
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
    list_of_hashtag_final = jsonify(Utils.wordCountDict(hashtag))
    list_of_hashtag_final.headers.add('Access-Control-Allow-Origin', '*')
    return list_of_hashtag_final


scheduler = BackgroundScheduler()
scheduler.add_job(func=updateData, trigger="interval", seconds=172800)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)
