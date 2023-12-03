

class BaseConfig:
    SECRET_KEY = "your secret key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False



class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234567890..asd@127.0.0.1:3306/flask?charset=utf8mb4"
    DEBUG = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[测试服务器MySQL用户名]:[测试服务器MySQL密码]@[测试服务器MySQL域名]:[测试服务器MySQL端口号]/pythonbbs?charset=utf8mb4"


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[生产环境服务器MySQL用户名]:[生产环境服务器MySQL密码]@[生产环境服务器MySQL域名]:[生产环境服务器MySQL端口号]/pythonbbs?charset=utf8mb4"