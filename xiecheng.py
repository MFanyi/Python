import json
import requests
import pymysql
import time

def spider(page,poiId,areaId):
    for i in range(1,page+1):
        header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
        request = {
            'arg': {'channelType': '2',
                    'collapseType': '0',
                    'commentTagId': '0',
                    'pageIndex': str(i),
                    'pageSize': '10',
                    'poiId': str(poiId),
                    'sortType': '3',
                    'sourceType': '1',
                    'starType': '0'},

            'head': {'auth': "",
                     'cid': "09031012411161407953",
                     'ctok': "",
                     'cver': "1.0",
                     'extension': [],
                     'lang': "01",
                     'sid': "8888",
                     'syscode': "09",
                     'xsid': ""}
        }
        response = requests.post(
            'https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList?_fxpcqlniredt=09031012411161407953',
            data=json.dumps(request))
        dict_list = json.loads(response.text)

        for comment in dict_list['result']['items']:
            imageSrcUrl = ''
            imageThumbUrl = ''
            for image in comment['images']:
                imageSrcUrl += image['imageSrcUrl'] + ','
                imageThumbUrl += image['imageThumbUrl'] + ','
            publishTime = comment['publishTime']
            if comment['scores']:
                score_area = str(comment['scores'][0]['score'])
                score_interest = str(comment['scores'][1]['score'])
                score_cost = str(comment['scores'][2]['score'])
            else:
                score_area = ""
                score_interest = ""
                score_cost = ""

            content = comment['content']
            publishTime = publishTime[6:16]

            createTime = time.localtime(int(publishTime))
            createTime = time.strftime("%Y-%m-%d %H:%M:%S", createTime)

            # 使用cursor()方法获取操作游标
            db = pymysql.connect("localhost", "root", "123456", 'tourism')
            cursor = db.cursor()
            # SQL插入语句
            sql = "insert into comment(user_id,area_id,content,image_src,create_time,image_thumb,score_area,score_interest,score_cost) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            try:
                cursor.execute(sql,
                               [2, areaId, content, imageSrcUrl, createTime, imageThumbUrl, score_area, score_interest, score_cost])
                db.commit()
            except:
                db.rollback()
            finally:
                db.close()
        # print(json.dumps(json.loads(json.dumps(dict_list['result']['items']), parse_int=str), indent=4, sort_keys=False,
        #                  ensure_ascii=False))
        print("第"+ str(i) + "页已爬取")

spider(300,77071,1)