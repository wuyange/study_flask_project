from flask import Blueprint, render_template

front = Blueprint("front", __name__, url_prefix="/front")

@front.route('/index')
def index():
    return 'index'