from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

db = SQLAlchemy()
mail = Mail()

def init_exts(app):
    db.init_app(app=app)
    mail.init_app(app=app)
    migrate = Migrate(app, db=db)