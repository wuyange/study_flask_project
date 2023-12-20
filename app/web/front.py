from flask import Blueprint, render_template, request, jsonify, current_app, url_for, g
import os

from app.models.post import BoardModel, db, PostModel
from app.forms.post import PostForm, ImageForm
from app.utils import random_file_name
from app.decorators import login_required

front = Blueprint("front", __name__, url_prefix="/front")

@front.route('/index')
def index():
    boards = [(-1, '所有板块')] + [(board.id,board.name) for board in BoardModel.query.all()]
    current_board = request.args.get('board', -1)
    posts = PostModel.query.all()
    data = {
        "posts": posts,
        "boards": boards,
        "current_board": current_board
    }
    print(data)
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
    