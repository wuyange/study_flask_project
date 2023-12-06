from flask import Blueprint, render_template
from app.forms.user import UserForms

user = Blueprint("user", __name__, url_prefix="/user")

@user.route('/register')
def register():
    from app.utils.mail import send_verification_code
    send_verification_code('2668643922@qq.com', None)
    return render_template("my/register.html", )

def send_mail():
    pass

@user.route('/login')
def login():
    return render_template("my/base.html", )