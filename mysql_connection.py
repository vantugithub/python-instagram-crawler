from collections import Counter
import psycopg2
import pymysql
from time import gmtime, strftime
import Utils
import config
import mysql.connector
import mysql_query
import pymysql

# connection = pymysql.connect(host='localhost',
#                              user='root',
#                              password='1111',
#                              db='instagram',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)


# session = Utils.instaLogin()
# if session.context.is_logged_in:
#     list_of_hashtag = Utils.fetchPostsData(session, str("music"), 50)
#     list_infoo = Utils.get_hashtag_final(list_of_hashtag)
#     number = []
#     for i in range(0, len(list_infoo)):
#         temp = list_infoo[i]['caption'].split()
#         for j in temp:
#             try:
#                 # if checkLanguage(str(j)) is True and str(hashtag).lower() not in j.lower():
#                 number.append(j)
#             except:
#                 continue
#     word_could_dict = Counter(number)
#     ok = list(reversed(sorted(word_could_dict.items(), key=lambda item: item[1])))
#     print(ok)
# else:
#     raise Exception("Authentication failure!")




# list_hashtag = ["netflix", "filmphotography", "technology", "tiktok"]
# session = Utils.instaLogin()
# date = 0
# if mysql_query.checkDateExist(connection) == 0:
#     mysql_query.insertDate(connection)
#     date += mysql_query.checkDateExist(connection)
# else:
#     date += mysql_query.checkDateExist(connection)
#
# for i in list_hashtag:
#     list_of_hashtag = Utils.fetchPostsData(session, str(i), 50)
#     list_of_hashtag_final = Utils.get_hashtag_final(list_of_hashtag)
#     # mysql_query.insertUserAndPost(list_of_hashtag_final, str(i))
#     number = []
#     for k in range(0, len(list_of_hashtag_final)):
#         temp = list_of_hashtag_final[k]['caption'].split()
#         for j in temp:
#             try:
#                 # if checkLanguage(str(j)) is True and str(hashtag).lower() not in j.lower():
#                 number.append(j)
#             except:
#                 continue
#     word_could_dict = Counter(number)
#     ok = list(reversed(sorted(word_could_dict.items(), key=lambda item: item[1])))
#     print(ok)
#     mysql_query.UpdateAnalysis(ok, date, int(mysql_query.getIdTopic(connection, i)))


# conn = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
#                         host=config.mysql_host)
#
# cur = conn.cursor()

connection = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
                              host=config.mysql_host)
cursor = connection.cursor()
cursor.execute("select * from topic where active = 1")
list_hashtag = cursor.fetchall()
print(list_hashtag)


date = 0
session = Utils.instaLogin()
if mysql_query.checkDateExist(connection) == 0:
    mysql_query.insertDate(connection)
    date += mysql_query.checkDateExist(connection)
else:
    date += mysql_query.checkDateExist(connection)

for i in list_hashtag:
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



# def create_connection():
#     try:
#         db = pymysql.connect(
#             host=config.mysql_host,
#             user=config.mysql_user,
#             password=config.mysql_password,
#             db=config.mysql_db,
#             charset='utf8mb4',
#             use_unicode=True,
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         return db
#     except:
#         print("can not connected database")
#         return None
