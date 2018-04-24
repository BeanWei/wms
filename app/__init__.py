import logging
from logging.handlers import RotatingFileHandler

import flask_whooshalchemyplus
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import APP_ENV, config

db = SQLAlchemy()

def setupLogging(level):
    '''创建日志记录'''
    logging.basicConfig(level=level)
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)

def create_app():
    '''工厂函数，创建APP实例'''
    setupLogging(config[APP_ENV].LOGGING_LEVEL)

    app = Flask(__name__)
    app.config.from_object(config[APP_ENV])

    CORS(app, resources=r'/*')

    db.init_app(app)
    
    flask_whooshalchemyplus.init_app(app)

    from app.api_v1 import api
    app.register_blueprint(api, url_prefix='/api/v1.0')

    return app