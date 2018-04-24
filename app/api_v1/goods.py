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
    '''
    t = request.args.get("t", default=None)
    f = request.args.get("f", default=None)

    # try:
    #     results = goods
