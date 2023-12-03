from app.exts import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Base(db.Model):
    __abstract__ = True
    create_time = db.Column(db.Integer, default=datetime.now)
    status = db.Column(db.SmallInteger, default=1)

    # def __init__(self):
    #     self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None