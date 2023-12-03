from app.exts import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Base(db.Model):
    # 在 Flask-SQLAlchemy 中，如果你的模型类中定义了abstract = True，
    # 那么这个类就会被视为抽象基类。抽象基类是一种特殊的类，它不能被直接实例化。
    # 相反，它是其他类的基类，这些类可以继承抽象基类的属性和方法。
    # 抽象基类通常被用来定义一个接口或公共行为。
    __abstract__ = True
    # create_time = db.Column(db.DATETIME, default=datetime.now)
    # status = db.Column(db.SmallInteger, default=1)

    # def __init__(self):
    #     self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    # def delete(self):
    #     self.status = 0

    # @property
    # def create_datetime(self):
    #     if self.create_time:
    #         return datetime.fromtimestamp(self.create_time)
    #     else:
    #         return None