from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def init_exts(app):
    db.init_app(app=app)