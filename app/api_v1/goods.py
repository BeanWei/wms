from app.models import Goods
from flask import jsonify,current_app,request

from . import api

@api.route('/')
def index():
    '''首页获取货物列表'''
    try:
        goodslist = Goods.query.all()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(code="500", msg="获取货物列表失败")
    goodss = [goods.to_json() for goods in goodslist]
    return jsonify(code="200", msg="获取货物列表成功", goodss=goodss)

@api.route('/search')
def search():
    '''搜索关键字获取货物
    :args get请求获取参数 /search?q=
    '''

    q = request.args.get("q", default=None)
    try:
        results = Goods.query.whoosh_search(q, fields=('title')).all()
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
        if t == price or t == stock or t == storage_time:
            if "to" not in f:
                return jsonify(code="403", msg="参数错误")
            else:
                rangeMin, rangeMax = f.split("to")
                goodss = Goods.query.filter_by(t >= rangeMin and t <= rangeMax).all()
        if t == storage_location:
            if f is None:
                return jsonify(code="403", msg="参数错误")
            else:
                goodss = Goods.query.filter_by(t=f).all()
        else:
            return jsonify(code="403", msg="参数错误")
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(code="500", msg="获取货物列表失败")

    goodss = [goods.to_json() for goods in goodss]
    return jsonify(code="200", msg="删选成功", count=len(goodss), goodss=goodss)