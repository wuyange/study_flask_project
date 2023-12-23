from . import BaseForm
from wtforms import ValidationError, SubmitField, StringField, PasswordField, IntegerField, BooleanField, FileField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import Length, Regexp, DataRequired, NoneOf
from app.models.post import BoardModel


class PostForm(BaseForm):
    title = StringField('title', validators=[DataRequired('请输入标题'),
                                    Length(min=2, max=100, message='请输入正确长度的标题！')])
    content = StringField('content', validators=[DataRequired('请输入内容')])
    board_id = IntegerField('board_id', validators=[DataRequired(message='请输入板块id!')])

    def validate_board_id(self, field):
        if field.data not in [board.id for board in BoardModel.query.all()]:
            raise ValidationError('请输入正确的板块id')

class ImageForm(BaseForm):
    image = FileField('image', validators=[FileRequired('上传文件不得为空'),
                                           FileAllowed(['png', 'jpg', 'svg'], '只允许上传PNG、JPG和SVG格式的图片')])

class CommentForm(BaseForm):
    content = StringField('content', validators=[DataRequired('请输入内容'),
                                                 Length(max=3000, message='评论内容应该小于等于3000')])