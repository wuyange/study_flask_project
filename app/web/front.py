from flask import Blueprint, render_template

front = Blueprint("front", __name__, url_prefix="/front")

# @front.route('/front')
# def register():
#     return render_template("front/register.html")