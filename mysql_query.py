import json

import psycopg2
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
        print("Failed")
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
        print("Failed")
        return 0


def insertUserAndPost(listUserAndPost):
    # try:
        connection = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
                                      host=config.mysql_host)
        sql_insert_post = "INSERT INTO posts_ins(iduser,codecaption,caption,user_instagrams_id) VALUES(%s,%s,%s,%s)"
        sql_insert_user = "INSERT INTO user_ins(user_ins,user_name) VALUES(%s,%s)"
        with connection.cursor() as cursor:
            for i in range(len(listUserAndPost)):
                check = checkUserExist(connection, listUserAndPost[i]['user'])
                if check != 0:
                    if len(listUserAndPost[i]['caption']) > 2:
                        cursor.execute(sql_insert_post, (int(check), listUserAndPost[i]['code'],
                                                         listUserAndPost[i]['caption'], int(check),))
                else:
                    if len(listUserAndPost[i]['caption']) > 2:
                        cursor.execute(sql_insert_user,
                                       (str(listUserAndPost[i]['user']), str(listUserAndPost[i]['user_name']),))
                        check_ = checkUserExist(connection, listUserAndPost[i]['user'])
                        cursor.execute(sql_insert_post, (int(check_), listUserAndPost[i]['code'],
                                                         listUserAndPost[i]['caption'], int(check_),))
                connection.commit()

    # except:
    #     connection.commit()
    #     connection.close()
    #     print("Failed")

# if __name__ == "__main__":
#     connection = mysql_connection.create_connection()
#     print(query_select(connection))
