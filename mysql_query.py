import json

import psycopg2
from time import gmtime, strftime

import pymysql

import config


def resetDataAndUpdateDataPerWeek():
    try:
        connection = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
                                      host=config.mysql_host)
        cursor = connection.cursor()
        cursor.execute("TRUNCATE posts_ins;")
        cursor.execute("DELETE FROM posts_ins;")
        cursor.execute("TRUNCATE TABLE posts_ins RESTART IDENTITY;")
        cursor.execute("TRUNCATE user_ins CASCADE;")
        cursor.execute("DELETE FROM user_ins;")
        connection.commit()
    except:
        connection.commit()
        connection.close()
        print("Failed reset and update data")


def query_select():
    try:
        connection = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
                                      host=config.mysql_host)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_ins")
            result = cursor.fetchall()
            return json.dumps(result)
    except:
        print("Failed query_select")
        return None


def checkUserExist(connection, user):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM user_ins WHERE user_ins = %s "
            cursor.execute(sql, (str(user),))
            result = cursor.fetchone()
            rows_affected = cursor.rowcount
            if rows_affected != 0:
                return result[0]
            else:
                return 0
    except:
        print("Failed checkUserExist")
        return 0


def getIdTopic(connection, name):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM topic WHERE name_topic = %s "
            cursor.execute(sql, (str(name),))
            result = cursor.fetchone()
            rows_affected = cursor.rowcount
            if rows_affected != 0:
                return result[0]
            else:
                return 0
    except:
        print("Failed getIdTopic")
        return 0


def getTopicActiveTrue(connection):
    try:
        with connection.cursor() as cursor:
            sql = "select * from topic where active = 1"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except:
        print("Failed get all topic")
        return 0


def checkDateExist(connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM date_of_analysis WHERE date = %s "
            cursor.execute(sql, (str(strftime("%Y-%m-%d", gmtime())),))
            result = cursor.fetchone()
            rows_affected = cursor.rowcount
            if rows_affected != 0:
                return result[0]
            else:
                return 0
    except:
        print("Failed checkDateExist")
        return 0


def insertDate(connection):
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO date_of_analysis(date) VALUES(%s) "
            cursor.execute(sql, (str(strftime("%Y-%m-%d", gmtime())),))
            connection.commit()
    except:
        print("Failed insert date")


def UpdateAnalysis(listWords, idDate, idTopic):
    try:
        connection = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
                                      host=config.mysql_host)
        with connection.cursor() as cursor:
            for i in range(0, 30):
                sql = "INSERT INTO analysis(count,name_hashtag,date_of_analysis_id,topic_id) VALUES(%s,%s,%s,%s) "
                cursor.execute(sql, (int(listWords[i][1]),
                                     str(listWords[i][0]),
                                     int(idDate),
                                     int(idTopic),))
            connection.commit()
            connection.close()
    except:
        connection.close()
        print("Failed UpdateAnalysis")


def insertUserAndPost(listUserAndPost, topic):
    try:
        connection = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
                                      host=config.mysql_host)
        # connection = pymysql.connect(host='localhost',
        #                              user='root',
        #                              password='1111',
        #                              db='instagram',
        #                              charset='utf8mb4',
        #                              cursorclass=pymysql.cursors.DictCursor)
        sql_insert_post = "INSERT INTO posts_ins(iduser,codecaption,caption,user_instagrams_id,topics_id) VALUES(%s," \
                          "%s,%s,%s,%s) "
        sql_insert_user = "INSERT INTO user_ins(user_ins,user_name) VALUES(%s,%s)"
        with connection.cursor() as cursor:
            for i in range(len(listUserAndPost)):
                check = checkUserExist(connection, listUserAndPost[i]['user'])
                if check != 0:
                    if len(listUserAndPost[i]['caption']) > 2:
                        try:
                            cursor.execute(sql_insert_post, (int(check),
                                                             listUserAndPost[i]['code'],
                                                             listUserAndPost[i]['caption'],
                                                             int(check),
                                                             int(getIdTopic(connection, topic)),))
                        except:
                            pass
                else:
                    if len(listUserAndPost[i]['caption']) > 2:
                        try:
                            cursor.execute(sql_insert_user,
                                           (str(listUserAndPost[i]['user']),
                                            str(listUserAndPost[i]['user_name']),))
                            check_ = checkUserExist(connection, listUserAndPost[i]['user'])
                            cursor.execute(sql_insert_post, (int(check_),
                                                             listUserAndPost[i]['code'],
                                                             listUserAndPost[i]['caption'],
                                                             int(check_),
                                                             int(getIdTopic(connection, topic)),))
                        except:
                            pass
                connection.commit()

    except:
        connection.commit()
        connection.close()
        print("Failed insertUserAndPost")

# if __name__ == "__main__":
#     connection = mysql_connection.create_connection()
#     print(query_select(connection))
