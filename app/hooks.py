from flask import session, g
from app.models.user import UserModel


def bbs_before_request():
    if "user_id" in session:
        user_id = session.get("user_id")
        try:
            user = UserModel.query.filter_by(uid=user_id).first()
            setattr(g, "user", user)
        except Exception:
            pass


def register_hooks(app):
    app.before_request(bbs_before_request)