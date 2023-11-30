from flask import Flask
from . import config
from .exts import init_exts
from .web import register_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.DevelopmentConfig)

    # 注册蓝图
    register_blueprint(app)

    # 初始化三方插件
    init_exts(app)
    return app