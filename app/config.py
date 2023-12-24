from datetime import timedelta
import os

class BaseConfig:
    SECRET_KEY = "123456"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = "2639773860@qq.com"
    MAIL_PASSWORD = "aqkxanorwfwvdhhh"
    MAIL_DEFAULT_SENDER = "2639773860@qq.com"

    # 设置登录超时时间
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # 设置上传文件
    UPLOAD_PATH = (os.path.dirname(os.path.abspath(__file__)) + 
                   os.path.sep + 'static' + 
                   os.path.sep + 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # 全局禁用CSRF保护
    WTF_CSRF_ENABLED = False

    # 每页的文章数量
    PER_PAGE_COUNT = 10
    
    # 头像设置
    AVATARS_SAVE_PATH = os.path.join(UPLOAD_PATH,"avatars")



class DevelopmentConfig(BaseConfig):
    # 缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "10.182.79.37"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = 123456
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@10.182.79.37:3306/flask?charset=utf8mb4"
    DEBUG = True


class TestingConfig(BaseConfig):
    # 缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_PASSWORD = 123456
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234567890..asd@127.0.0.1:3306/flask?charset=utf8mb4"


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[生产环境服务器MySQL用户名]:[生产环境服务器MySQL密码]@[生产环境服务器MySQL域名]:[生产环境服务器MySQL端口号]/pythonbbs?charset=utf8mb4"
