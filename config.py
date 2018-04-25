import logging

APP_ENV = "testing"

class BaseConfig:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #是否开启跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(BaseConfig):
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Bean:124127@127.0.0.1:3306/wms"

class DevelopmentConfig(BaseConfig):
    DEBUG = False
    LOGGING_LEVEL = logging.WARNING
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Bean:124127@127.0.0.1:3306/wms"

config = {
    "testing": TestingConfig,
    "devolopment": DevelopmentConfig,
}