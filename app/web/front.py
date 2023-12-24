from flask import Blueprint, render_template, request, jsonify, current_app, url_for, g, redirect
from sqlalchemy import or_
import os

from app.models.post import BoardModel, db, PostModel, CommentModel
from app.forms.post import PostForm, ImageForm, CommentForm
from app.utils import random_file_name
from app.decorators import login_required

front = Blueprint("front", __name__, url_prefix="/front")

@front.route('/index')
def index():
    boards = [(-1, '所有板块')] + [(board.id,board.name) for board in BoardModel.query.all()]

    # 接受get请求参数
    current_board = int(request.args.get('board', -1))
    page = int(request.args.get('page', 1))
    keyword = request.args.get('keyword', None)


    # 筛选
    query = PostModel.query
    # https://blog.csdn.net/gymaisyl/article/details/96601798
    if keyword:
        query = query.filter(or_(PostModel.title.like(f"%{keyword}%"),
                                 PostModel.content.like(f"%{keyword}%")))

    if current_board != -1:
        query = query.filter(PostModel.board_id==current_board)

    # 排序
    query = query.order_by(PostModel.create_time.desc())

    # 分页 https://blog.csdn.net/weixin_44420527/article/details/106886332
    paginate = query.paginate(page=page, per_page=current_app.config['PER_PAGE_COUNT'])
    data = {
        "boards": boards,
        "current_board": current_board,
        "paginate": paginate
    }
    return render_template('my/index.html', **data)

@front.route('/add_post', methods=["post", 'get'])
@login_required
def add_post():
    form = PostForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            with db.auto_commit():
                title = form.title.data
                content = form.content.data
                board_id = form.board_id.data
                author_id = g.get('user').id
                post = PostModel(title=title, content=content,
                                 board_id=board_id, author_id=author_id)
                db.session.add(post)
            return 'success', 200
        else:
            return jsonify(form.errors), 400
    boards = BoardModel.query.all()
    return render_template("my/post_public.html", form=form, boards=boards)

@front.post('/upload/image')
@login_required
def upload_image():
    form = ImageForm(request.files)
    if form.validate_on_submit():
        f = form.image.data
        filename = random_file_name(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_PATH'], 'images', filename))
        url = url_for('static', filename=f'uploads/images/{filename}')
        data = {
            "errno": 0, 
            "data": {
                "url": url, 
                "alt": "", 
                "href": ""
            }
        }
        return jsonify(data)
    return jsonify({
        "errno": 1, 
        "message": [error for error in form.errors]
    })

@front.route('/post/<int:post_id>', methods=['get'])
def post_detail(post_id):
    post = PostModel.query.filter(PostModel.id == post_id).first_or_404()
    # 增加阅读量
    with db.auto_commit():
        post.read_count += 1
    # 返回评论
    comments = CommentModel.query.filter(CommentModel.post_id==post_id).order_by(CommentModel.create_time.desc()).all()
    return render_template('my/post_detail.html', post=post, comments=comments)

@front.post('/add_comment/<int:post_id>')
@login_required
def add_comment(post_id):
    form = CommentForm(request.form)
    flag = PostModel.query.get_or_404(post_id)
    if form.validate_on_submit():
        with db.auto_commit():
            user_id = g.get('user').id
            comment = CommentModel(content=form.content.data, post_id=post_id,
                                   author_id=user_id)
            db.session.add(comment)
    return redirect(url_for('front.post_detail', post_id=post_id))
