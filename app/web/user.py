from flask import Blueprint, render_template
from app.forms.user import UserForms

user = Blueprint("user", __name__, url_prefix="/user")

@user.route('/register')
def register():
    return render_template("my/register.html", )

@user.route('/login')
def login():
    return render_template("my/base.html", )