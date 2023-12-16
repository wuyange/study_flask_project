from . import BaseForm
from wtforms import ValidationError, SubmitField, StringField, PasswordField, IntegerField, BooleanField, FileField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import Email, EqualTo, Length, Regexp, DataRequired
from app.models.user import UserModel
from app.utils import redis

class PostForm(BaseForm):
    pass

class ImageForm(BaseForm):
    image = FileField('image', validators=[FileRequired('上传文件不得为空'),
                                           FileAllowed(['png', 'jpg', 'svg'], '只允许上传PNG、JPG和SVG格式的图片')])