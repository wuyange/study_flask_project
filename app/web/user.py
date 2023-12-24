import os
from flask import Blueprint, current_app, render_template, make_response, request, redirect, url_for, session, g
from werkzeug.datastructures import CombinedMultiDict

from app.decorators import login_required
from app.forms.user import UserRegisterForms, UserLoginForms, EditUserFrom
from app.utils import mail, random_file_name, redis
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
    redis.set(request.form['email'], code, timeout=120)
    return make_response(), 200

@user.route('/login', methods=['get', 'post'])
def login():
    form = UserLoginForms()
    if form.validate_on_submit():
        session['user_id'] = UserModel.query.filter_by(username=form.username.data).first().uid
        if form.remember.data:
            session.permanent = True
        return redirect(url_for('front.index'))
    print(session.get('user_id', None))
    return render_template("my/login.html", form=form)

@user.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))

@user.route('/<string:user_uid>', methods=['get', 'post'])
@login_required
def personal_center(user_uid):
    form = EditUserFrom(CombinedMultiDict([request.form, request.files]))
    if form.validate_on_submit():
        avatar = form.avatar.data
        username = form.username.data
        signature = form.signature.data

        with db.auto_commit():

            if g.user.username != username:
                g.user.username = username

            if avatar:
                filename = random_file_name(avatar.filename)
                file_path = os.path.join(current_app.config['UPLOAD_PATH'], 'avatar', filename)
                avatar.save(file_path)
                avatar = 'uploads/'+'avatar/'+filename
                g.user.avatar = avatar

            if signature:
                g.user.signature = signature

        return redirect(url_for('user.personal_center', user_uid=user_uid))   
    user = UserModel.query.filter(UserModel.uid==user_uid).first_or_404()
    flag = False
    if hasattr(g, "user") and g.user.uid == user_uid:
        flag = True
    return render_template('my/personal_center.html', user=user, flag=flag)