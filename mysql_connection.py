import config
import pymysql.cursors
import psycopg2

# import Utils
# import mysql_query
#
# session = Utils.instaLogin()
# mysql_query.resetDataAndUpdateDataPerWeek()
# list_of_hashtag = Utils.fetchPostsData(session, "netflix", 30)
# list_of_hashtag_final = Utils.get_hashtag_final(list_of_hashtag)
# mysql_query.insertUserAndPost(list_of_hashtag_final)

# conn = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
#                         host=config.mysql_host)

# cur = conn.cursor()

# def create_connection():
#     try:
#         conn = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
#                                 host=config.mysql_host)
#         return conn
#     except:
#         print("can not connected database")
#         return None


# connection = create_connection()
# cursor = connection.cursor()

# connection = psycopg2.connect(dbname=config.mysql_db, user=config.mysql_user, password=config.mysql_password,
#                               host=config.mysql_host)
# cursor = connection.cursor()
# cursor.execute("TRUNCATE posts_ins;")
# cursor.execute("DELETE FROM posts_ins;")
# cursor.execute("TRUNCATE TABLE posts_ins RESTART IDENTITY;")
# cursor.execute("TRUNCATE user_ins CASCADE;")
# cursor.execute("DELETE FROM user_ins;")
# connection.commit()
# connection.close()
# connection.commit()

# cur.execute("CREATE TABLE test(id SERIAL PRIMARY KEY, name VARCHAR);")
# cur.execute("insert into test(name) values(%s) ", ("van nu",))
# sql_insert_user = "insert into test(name) values(%s)"
# cur.execute(sql_insert_user, ("nguyen van tu",))
# cur.execute("SELECT * FROM test;")
# print(cur.fetchall())
# cur.execute("TRUNCATE test;")
# cur.execute("DELETE FROM test;")
# cur.execute("TRUNCATE TABLE test RESTART IDENTITY;")
# connection.commit()
# connection.close()

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
