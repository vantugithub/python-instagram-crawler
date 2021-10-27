from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests
import time as times
from datetime import datetime
import json
import re
from langdetect import detect
import instaloader


def remove_emoji_username(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def get_hashtag(text):
    text = text.split()
    text_ = ""
    for tx in text:
        if "#" in tx:
            text_ += tx + " "
    text_ = text_.split('#')
    rs = ""
    for tx in text_:
        tx = tx.replace(" ", "")
        if len(tx) > 0:
            rs += tx + " "
    rs = remove_emoji(rs)
    rs_lis = rs.split()
    result = ""
    for i in rs_lis:
        if len(i) > 0:
            try:
                dectect_language = str(detect(i))
                if checkLanguage(dectect_language) is False:
                    continue
                else:
                    result += i + " "
            except:
                continue
    return result


def checkLanguage(language):
    list_language_code = ["th", "ar", "ko", "ur", "ja", "zh-cn", "fa", "tr", "zh-tw", "ru"]
    for i in list_language_code:
        if str(language) == i:
            return False
    return True


def instaLogin():
    print("Logging in...")

    ses = instaloader.Instaloader()
    ses.context.sleep = False
    ses.login("nangnaggg", "q121222112")

    print("...done")

    return ses


def fetchPostsData(session, hashtag, number_data):
    print("Fetching posts data...")
    list_info = []
    data_temp = session.context.get_json(path="explore/tags/" + hashtag + "/", params={"__a": 1})
    hasNextPage = True
    pageNumber = 1

    while True:
        try:
            if len(list_info) > int(number_data):
                break
            # print("Page " + str(pageNumber))
            for i in range(len(data_temp.get("data").get("top").get("sections"))):
                try:
                    for j in range(len(
                            data_temp.get("data").get("top").get("sections")[i].get("layout_content").get("medias"))):
                        info = {}
                        info["code"] = \
                            data_temp.get("data").get("top").get("sections")[i].get("layout_content").get("medias")[
                                j].get(
                                "media").get("code")

                        # print(data_temp.get("data").get("top").get("sections")[i].get("layout_content").get("medias")[
                        #           j].get("media").get("code"))

                        info["user"] = \
                            data_temp.get("data").get("top").get("sections")[i].get("layout_content").get("medias")[
                                j].get(
                                "media").get("user").get("username")
                        info["user_name"] = \
                            data_temp.get("data").get("top").get("sections")[i].get("layout_content").get("medias")[
                                j].get(
                                "media").get("user").get("full_name")
                        info["caption"] = ""
                        if data_temp.get("data").get("top").get("sections")[i].get("layout_content").get("medias")[
                            j].get("media").get("caption") is not None:
                            info["caption"] = \
                                data_temp.get("data").get("top").get("sections")[i].get("layout_content").get("medias")[
                                    j].get("media").get("caption").get("text")

                        info["list_media"] = []
                        if data_temp.get("data").get("top").get("sections")[i].get("layout_content").get("medias")[
                            j].get("media").get("carousel_media_count") is not None:
                            for media_count in range(
                                    data_temp.get("data").get("top").get("sections")[i].get("layout_content").get(
                                        "medias")[j].get("media").get("carousel_media_count")):
                                info["list_media"].append({'url':
                                                               data_temp.get("data").get("top").get("sections")[i].get(
                                                                   "layout_content").get("medias")[j].get("media").get(
                                                                   "carousel_media")[media_count].get(
                                                                   "image_versions2").get("candidates")[0].get("url")})
                        else:
                            info["list_media"].append({'url': data_temp.get("data").get("top").get("sections")[i].get(
                                "layout_content").get("medias")[j].get("media").get("image_versions2").get(
                                "candidates")[0].get("url")})
                        list_info.append(info)
                except:
                    break

            for i in range(len(data_temp.get("data").get("recent").get("sections"))):
                try:
                    for j in range(len(data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get(
                            "medias"))):
                        info = {}
                        info["code"] = \
                            data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get("medias")[
                                j].get("media").get("code")

                        # print(
                        #     data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get("medias")[
                        #         j].get("media").get("code"))

                        info["user"] = \
                            data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get("medias")[
                                j].get("media").get("user").get("username")
                        info["user_name"] = \
                            data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get("medias")[
                                j].get("media").get("user").get("full_name")
                        info["caption"] = ""
                        if data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get("medias")[
                            j].get("media").get("caption") is not None:
                            info["caption"] = \
                                data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get(
                                    "medias")[
                                    j].get("media").get("caption").get("text")

                        info["list_media"] = []
                        if data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get("medias")[
                            j].get("media").get("carousel_media_count") is not None:
                            for media_count in range(
                                    data_temp.get("data").get("recent").get("sections")[i].get("layout_content").get(
                                        "medias")[j].get("media").get("carousel_media_count")):
                                info["list_media"].append({'url': data_temp.get("data").get("recent").get("sections")[
                                    i].get("layout_content").get("medias")[j].get("media").get("carousel_media")[
                                    media_count].get("image_versions2").get("candidates")[0].get("url")})
                        else:
                            info["list_media"].append({'url':
                                                           data_temp.get("data").get("recent").get("sections")[i].get(
                                                               "layout_content").get("medias")[j].get("media").get(
                                                               "image_versions2").get("candidates")[0].get("url")})
                        list_info.append(info)
                except:
                    break

            hasNextPage = data_temp['data']['recent']['more_available']

            if hasNextPage:
                data_temp = session.context.get_json(
                    path="explore/tags/" + hashtag + "/",
                    params={"__a": 1,
                            "max_id": data_temp['data']['recent']['next_max_id']}
                )
                times.sleep(3)
            pageNumber += 1
        except:
            break
    return list_info


def get_hashtag_final(list_info):
    list_ = list_info
    for i in range(len(list_)):
        # print(get_hashtag(list_[i]['caption']))
        list_[i]['caption'] = get_hashtag(list_[i]['caption'])
        list_[i]['user_name'] = remove_emoji_username(list_[i]['user_name'])
    return list_


def main(number_data, hashtag):
    session = instaLogin()

    if session.context.is_logged_in:
        fetchPostsData(session, str(hashtag), number_data)
    else:
        raise Exception("Authentication failure!")


def wordCountDict(hashtag):
    session = instaLogin()
    if session.context.is_logged_in:
        list_of_hashtag = fetchPostsData(session, str(hashtag), 60)
        list_infoo = get_hashtag_final(list_of_hashtag)
        number = []
        for i in range(0, len(list_infoo)):
            temp = list_infoo[i]['caption'].split()
            for j in temp:
                try:
                    # if checkLanguage(str(j)) is True and str(hashtag).lower() not in j.lower():
                    number.append(j)
                except:
                    continue
        word_could_dict = Counter(number)
        ok = list(reversed(sorted(word_could_dict.items(), key=lambda item: item[1])))
        return ok
    else:
        raise Exception("Authentication failure!")
        return None
    # ok_ = []
    # for i in range(20):
    #     if len(ok[i][0]) > 0:
    #         try:
    #             if str(detect(ok[i][0])) != "th" and "netflix" not in ok[i][0].lower():
    #                 ok_.append(ok[i])
    #         except:
    #             continue

# if __name__ == "__main__":
#     list_of_hashtag = login_ins(str("netflix"), 50)
#     list_infoo = get_hashtag_final(list_of_hashtag)
#     number = []
#     for i in range(0, len(list_infoo)):
#         temp = list_infoo[i]['caption'].split()
#         for j in temp:
#             try:
#                 if checkLanguage(str(j)) is True and "netflix" not in j.lower():
#                     number.append(j)
#             except:
#                 continue
#
#     word_could_dict = Counter(number)
# plt.figure(figsize=(20, 20))
# Wc = WordCloud(max_words=500, width=1600, height=800
#                , background_color='white').generate_from_frequencies(word_could_dict)
#
# plt.axis("off")
# plt.imshow(Wc, interpolation='bilinear')
# plt.savefig("img/ita_wine.png", format="png")
# ok = list(reversed(sorted(word_could_dict.items(), key=lambda item: item[1])))
# ok_ = []
# for i in range(20):
#     if len(ok[i][0]) > 0:
#         try:
#             if str(detect(ok[i][0])) != "th" and "netflix" not in ok[i][0].lower():
#                 ok_.append(ok[i])
#         except:
#             continue
