from flask import Blueprint

user = Blueprint("user", __name__, url_prefix="/user")

@user.route('/user')
def test():
    return 'user'