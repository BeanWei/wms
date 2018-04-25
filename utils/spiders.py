'''
api接口
https://s.taobao.com/api?_ksTS=1523179236254_226&callback=jsonp227&ajax=true&m=customized&stats_%27%20\%20%27click=search_radio_all:1&q=%E7%BC%96%E7%A8%8B&s=36&imgfile=&initiative_id=staobaoz_20180425&bcoffset=-1%27%20\%20%27&js=1&ie=utf8&rn=d5706a3802513dad625d594a35702a6b
'''
import pymysql
from datetime import datetime
import re
import urllib.request

true = True
false = False
null = None


conn = pymysql.connect(
        host='127.0.0.1', port=3306,
        user='Bean', password='124127',
        db='wms', use_unicode=True, charset="utf8")
cursor = conn.cursor()
for page in range(0, 4500):
    api = r'https://s.taobao.com/api?_ksTS=1523179236254_226&callback=jsonp227&ajax=true&m=customized&stats_%27%20\%20%27click=search_radio_all:1&q=%E4%BD%8E%E4%BB%B7&s={}&imgfile=&initiative_id=staobaoz_20180425&bcoffset=-1%27%20\%20%27&js=1&ie=utf8&rn=d5706a3802513dad625d594a35702a6b'.format(page)
    rep = urllib.request.urlopen(api).read().decode('utf-8')
    result = eval(re.findall(r'jsonp227(.*?);', rep)[0][1:-1].strip().replace("\n", ""))
    for r in result['API.CustomizedApi']['itemlist']['auctions']:   
        #r = result['API.CustomizedApi']['itemlist']['auctions'][0]
        title = r["raw_title"]#re.sub(r'<[^>]+>', '', r["title"])
        price = r["view_price"]
        stock = r["comment_count"]
        storage_time = datetime.utcnow()
        if " " in r["item_loc"]:
            storage_location = r["item_loc"].split(" ")[-1]
        else:
            storage_location = r["item_loc"]
        print(title,'/',price,'/',stock,'/',storage_location)
        sql = "INSERT INTO goods(title,price,stock,storage_time,storage_location) VALUES ('%s', '%s', '%s', '%s', '%s')" % (title, price, stock, storage_time, storage_location)
        cursor.execute(sql)
        conn.commit()
# sql = "UPDATE wms SET storage_location = '重庆' WHERE storage_location = ''"
# try:
#     cursor.execute(sql)
#     conn.commit()
# except:
#     conn.rollback()
conn.close()





