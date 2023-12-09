from flask_wtf import FlaskForm
from wtforms import ValidationError, SubmitField, StringField, PasswordField
from wtforms.validators import Email, EqualTo, Length, Regexp

class UserRegisterForms(FlaskForm):
    email = StringField('')


class UserLoginForms(FlaskForm):
    pass
