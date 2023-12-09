from flask import Blueprint, render_template, make_response, request, redirect, url_for, session
from app.forms.user import UserRegisterForms, UserLoginForms
from app.utils import mail, redis
from app.models.user import UserModel, db

user = Blueprint("user", __name__, url_prefix="/user")

@user.route('/register', methods=['get', 'post'])
def register():
    form = UserRegisterForms(request.form)
    if form.validate_on_submit():
        with db.auto_commit():
            user = UserModel(username=form.user_name.data,
                             email=form.email.data,
                             password=form.password.data)
            db.session.add(user)
        return redirect(url_for('user.login'))
    return render_template("my/register.html", form=form)

@user.route('/send_verification_code', methods=['post'])
def send_verification_code():
    # 随机4位验证码
    from random import randint
    code = [randint(0,9) for _ in range(4)]
    code = "".join(map(str, code))
    mail.send_verification_code(request.form['email'], code)
    redis.set(request.form['email'], code, timeout=60)
    return make_response(), 200

@user.route('/login', methods=['get', 'post'])
def login():
    form = UserLoginForms()
    if form.validate_on_submit():
        print('xxxxxxx')
        session['user_id'] = UserModel.query.filter_by(username=form.username.data).first().uid
        if form.remember.data:
            session.permanent = True
        return redirect(url_for('front.index'))
    return render_template("my/login.html", form=form)
