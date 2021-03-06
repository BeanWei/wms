from app.models import Goods
from flask import jsonify,current_app,request

import re
import urllib

from . import api
from app import db

@api.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        '''首页获取货物列表'''
        try:
            goodslist = Goods.query.all()
        except Exception as e:
            current_app.logger.debug(e)
            return jsonify(code="500", msg="获取货物列表失败")
        goodss = [goods.to_json() for goods in goodslist]
        return jsonify(code="200", msg="获取货物列表成功", goodss=goodss)

    if request.method == 'POST':
        '''新增货物'''
        title = request.values.get("title")
        price= request.values.get("price")
        stock = request.values.get("stock")
        storage_location = request.values.get("storage_location")
        if not all ([title, price, stock, storage_location]):
            return jsonify(code="403", msg="参数错误")
        goods = Goods()
        goods.title = title
        goods.price = price
        goods.stock = stock
        goods.storage_location = storage_location

        try:
            db.session.add(goods)
            db.session.commit()
        except Exception as e:
            current_app.logger.debug(e)
            db.session.rollback()
            return jsonify(code="500", msg="添加货物失败")
        
        return jsonify(code="200", msg="添加货物成功")

@api.route('/search')
def search():
    '''搜索关键字获取货物
    :args get请求获取参数 /search?q=
    '''

    q = request.args.get("q", default=None)
    try:
        results = Goods.query.whoosh_search(q, or_=True).all()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(code="500", msg="获取货物列表失败")
    if not results:
        return jsonify(code="200", msg="搜索成功,结果为空")
    results = [result.to_json() for result in results]

    return jsonify(code="200", msg="搜素成功,已找到结果", count=len(results), results=results)

@api.route('/filter')
def filters():
    '''按需求筛选
    :args get请求获取筛选参数 /filter?t=&f=
    : t是筛选类型，f是参数
    t-> price,stock,storage_time,storage_location
    f-> t为前三者的时候f为范围值(例如:"100to500"),f为库存地的时候t为地点(例如:"北京")
    '''
    t = request.args.get("t", default=None)
    f = request.args.get("f", default=None)

    try:
        if t == "price" or t == "stock" or t == "storage_time":
            if "to" not in f:
                return jsonify(code="403", msg="参数错误")
            else:
                rangeMin, rangeMax = f.split("to")
                if t == "price":
                    goodss = Goods.query.filter(Goods.price.between(rangeMin, rangeMax)).all()
                elif t == "stock":
                    goodss = Goods.query.filter(Goods.stock.between(rangeMin, rangeMax)).all()
                elif t == "storage_time":
                    goodss = Goods.query.filter(Goods.storage_time.between(rangeMin, rangeMax)).all()
        elif t == "storage_location":
            if f is None:
                return jsonify(code="403", msg="参数错误")
            else:
                goodss = Goods.query.filter_by(storage_location=f).all()
        else:
            return jsonify(code="403", msg="参数错误")
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(code="500", msg="获取货物列表失败")

    goodss = [goods.to_json() for goods in goodss]
    return jsonify(code="200", msg="删选成功", count=len(goodss), goodss=goodss)





'''爬虫获取数据'''
@api.route('/spiders', methods=['POST'])
def spiders():

    # eval(str转dict)需要的参数
    true = True
    false = False
    null = None

    qthing = request.values.get('q')
    api = r'https://s.taobao.com/api?_ksTS=1523179236254_226&callback=jsonp227&ajax=true&m=customized&stats_%27%20\%20%27click=search_radio_all:1&q={}&s=1&imgfile=&initiative_id=staobaoz_20180425&bcoffset=-1%27%20\%20%27&js=1&ie=utf8&rn=d5706a3802513dad625d594a35702a6b'.format(urllib.request.quote(qthing))
    current_app.logger.debug(api)
    rep = urllib.request.urlopen(api).read().decode('utf-8')
    result = eval(re.findall(r'jsonp227(.*?);', rep)[0][1:-1].strip().replace("\n", ""))
    for r in result['API.CustomizedApi']['itemlist']['auctions']:   
        #r = result['API.CustomizedApi']['itemlist']['auctions'][0]
        title = r["raw_title"]#re.sub(r'<[^>]+>', '', r["title"])
        price = r["view_price"]
        stock = r["comment_count"]
        if " " in r["item_loc"]:
            storage_location = r["item_loc"].split(" ")[-1]
        else:
            storage_location = r["item_loc"]

        goods = Goods()
        goods.title = title
        goods.price = price
        goods.stock = stock
        goods.storage_location = storage_location

        try:
            db.session.add(goods)
            db.session.commit()
        except Exception as e:
            current_app.logger.debug(e)
            db.session.rollback()
            return jsonify(code="500", msg="添加货物失败")
        
    return jsonify(code="200", msg="添加货物成功")