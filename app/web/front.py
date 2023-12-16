from flask import Blueprint, render_template, request, jsonify, current_app, url_for
import os

from app.models.post import BoardModel
from app.forms.post import PostForm, ImageForm
from app.utils import random_file_name

front = Blueprint("front", __name__, url_prefix="/front")

@front.route('/index')
def index():
    return 'index'

@front.route('/add_post', methods=["post", 'get'])
def add_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        pass
    # boards = BoardModel.query.all()
    boards = {}
    return render_template("my/post_public.html", form=form, boards=boards)

@front.post('/upload/image')
def upload_image():
    print(request.files.get('image'))
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
    print(form.errors)
    return jsonify({
        "errno": 1, 
        "message": [error for error in form.errors]
    })
    