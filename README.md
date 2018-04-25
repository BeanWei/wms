# WMS(货物管理系统）
--------------------------------------------
## 学习Flask全文搜索的练手Demo，基于Jieba和flask_whooshalchemyplus来做分词和搜索

* 效果图
![Alt text](https://github.com/BeanWei/wms/blob/master/Screenshots/OK.PNG)

- API:
    * ['GET', 'POST']   127.0.0.1:5000/api/v1.0/        获取和添加货物
    * ['GET']           127.0.0.1:5000/api/v1.0/filter?t=&f=        根据需求筛选     
        * : t是筛选类型，f是参数
        * t-> price,stock,storage_time,storage_location
        * f-> t为前三者的时候f为范围值(例如:"100to500"),f为库存地的时候t为地点(例如:"北京")
    * ['GET']           127.0.0.1:5000/api/v1.0/search?q=           根据关键字 `q` 进行全文搜索，中英文皆可
    * ['POST']          127.0.0.1:5000/api/v1.0/spiders             启动爬虫获取某宝商品信息拿过来做数据源
        * post参数为 `q` ,随意搜索任何内容，返回12条内容(api中的s参数为页数，可修改然后循环爬取,我的是固定的)

- 通过post提交的数据包括爬虫获取的数据都能被 `flask_whooshalchemyplus` 建立起所选字段的索引

---------------------------------------------------------
## TODO :
- [ ] 前端界面的完善[vue + element-ui]
- [ ] 参考真的WMS来完善这个货物管理系统