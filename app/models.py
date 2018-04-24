from datetime import datetime
from jieba.analyse.analyzer import ChineseAnalyzer

from . import db

class Goods(db.Model):
    '''货物模型'''
    __tablename__ = 'goods'
    __searchable__ = ['title']    #搜索字段
    __analyzer__ = ChineseAnalyzer()   #引入中文分词

    id = db.Column(db.Integer, index=True, primary_key=True)
    title = db.Column(db.Text)
    price = db.Column(db.Float, index=True)
    stock = db.Column(db.Integer, index=True) 
    storage_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    storage_location = db.Column(db.String(225), index=True)

    meta = {
        'ordering': ['-storage_time']
    }

    def to_json(self):
        '''返回货物信息'''
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'stock': self.stock,
            'storage_time': self.storage_time,
            'storage_location': self.storage_location
        }