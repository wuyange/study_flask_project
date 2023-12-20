from flask import Flask
from . import config
from .exts import init_exts
from .web import register_blueprint
from .cli import register_cli
from .hooks import register_hooks


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.TestingConfig)

    # 注册蓝图
    register_blueprint(app)

    # 初始化三方插件
    init_exts(app)

    # 注册命令行
    register_cli(app)

    # 注册钩子函数
    register_hooks(app)
    return app