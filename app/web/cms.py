from flask import Blueprint

cms = Blueprint("cms", __name__, url_prefix="/cms")


@cms.route('/cms')
def test():
    return 'cms'