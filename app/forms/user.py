from . import BaseForm
from wtforms import ValidationError, SubmitField, StringField, PasswordField, IntegerField
from wtforms.validators import Email, EqualTo, Length, Regexp, DataRequired

class UserRegisterForms(BaseForm):
    email = StringField('email', validators=[DataRequired('邮箱不得为空'),Email('邮箱格式不正确')])
    code = StringField('code', validators=[DataRequired('验证码不得为空'),
                                           Length(min=4, max=4, message="验证码格式错误"),
                                           Regexp(regex=r'^\d{4}$', message='验证码格式错误')])
    user_name = StringField('user_name', validators=[DataRequired('用户名不得为空'),
                                                     Regexp(r'^[a-zA-Z0-9_]+$', message='用户名只能为数字、字母和下划线'),
                                                     Length(min=2, max=20, message='用户名长度为2-20')])
    password = PasswordField('password', validators=[DataRequired('密码不得为空'), 
                                                     Length(min=6, max=20, message='密码长度为6-20'),
                                                     Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,20}$')])
    password_confirm = PasswordField('password_confirm', validators=[EqualTo(password, message='两次输入密码不一致')])
    register = SubmitField('register')


class UserLoginForms(BaseForm):
    pass
