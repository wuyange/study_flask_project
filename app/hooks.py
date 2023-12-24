from flask import session, g, render_template
from app.models.user import UserModel


def bbs_before_request():
    if "user_id" in session:
        user_id = session.get("user_id")
        try:
            user = UserModel.query.filter_by(uid=user_id).first()
            setattr(g, "user", user)
        except Exception:
            pass

def handle_error(error):
    return render_template('errors/exception.html')

def handle_401_error(error):
    return render_template('errors/401.html')

def handle_404_error(error):
    return render_template('errors/404.html')

def handle_405_error(error):
    return render_template('errors/405.html')

def handle_500_error(error):
    return render_template('errors/500.html')


def register_hooks(app):
    app.before_request(bbs_before_request)

    # 异常处理
    app.errorhandler(Exception)(handle_error)
    app.errorhandler(401)(handle_401_error)
    app.errorhandler(404)(handle_404_error)
    app.errorhandler(405)(handle_405_error)
    app.errorhandler(500)(handle_500_error)
    