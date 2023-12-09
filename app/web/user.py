from flask import Blueprint, render_template, make_response, request
from app.forms.user import UserRegisterForms
from app.utils import mail, redis

user = Blueprint("user", __name__, url_prefix="/user")

@user.route('/register')
def register():
    return render_template("my/register.html", )

@user.route('/send_verification_code', methods=['post'])
def send_verification_code():
    # 随机4位验证码
    from random import randint
    code = [randint(0,9) for _ in range(4)]
    code = "".join(map(str, code))
    mail.send_verification_code(request.form['email'], code)
    redis.set(request.form['email'], code)
    print(redis.get(request.form['email']))
    return make_response(), 200

@user.route('/login')
def login():
    return render_template("my/base.html", )