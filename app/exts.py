from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def init_exts(app):
    db.init_app(app=app)
    migrate = Migrate(app, db=db)