from . import BaseForm
from wtforms import ValidationError, SubmitField, StringField, PasswordField, FileField, BooleanField
from wtforms.validators import Email, EqualTo, Length, Regexp, DataRequired
from flask_wtf.file import FileRequired, FileAllowed

from app.models.user import UserModel
from app.utils import redis

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
                                                     Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,20}$',
                                                            message="密码必须包含数字、大写字母、小写字母和特殊字符")])
    password_confirm = PasswordField('password_confirm', validators=[EqualTo('password', message='两次输入密码不一致')])
    register = SubmitField('register')
    return_login = SubmitField('return_login')

    def validate_email(self, field):
        if UserModel.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册')

    def validate_code(self, field):
        if field.data != redis.get(self.email.data):
            raise ValidationError('验证码错误')

    def validate_user_name(self, field):
        if UserModel.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经被注册')


class UserLoginForms(BaseForm):
    username = StringField('username', validators=[DataRequired('用户名不得为空'),
                                                     Regexp(r'^[a-zA-Z0-9_]+$', message='用户名只能为数字、字母和下划线'),
                                                     Length(min=2, max=20, message='用户名长度为2-20')])
    password = PasswordField('password', validators=[DataRequired('密码不得为空'),
                                                     Length(min=6, max=20, message='密码长度为6-20'),
                                                     Regexp(
                                                         r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,20}$',
                                                         message="密码必须包含数字、大写字母、小写字母和特殊字符")])
    remember = BooleanField('remember')

    def validate(self, extra_validators=None):
        # 首先调用父类的validate方法
        if not super(UserLoginForms, self).validate():
            return False

        username = UserModel.query.filter_by(username=self.username.data).first()
        if not username or not username.check_password(self.password.data):
            self.password.errors.append('用户名或者密码错误')
            return False

        return True
    
class EditUserFrom(BaseForm):
    username = StringField('user_name', validators=[DataRequired('用户名不得为空'),
                                                     Regexp(r'^[a-zA-Z0-9_]+$', message='用户名只能为数字、字母和下划线'),
                                                     Length(min=2, max=20, message='用户名长度为2-20')])
    signature = StringField('signature', validators=[Length(max=100, message='个性签名长度不能超过100个字符')])
    avatar = FileField('avatar', validators=[FileAllowed(['jpg', 'png', 'svg'], message='只允许上传PNG、JPG和SVG格式的图片')])