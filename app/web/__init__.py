

def register_blueprint(app):
    from .cms import cms
    from .front import front
    from .user import user
    app.register_blueprint(cms)
    app.register_blueprint(front)
    app.register_blueprint(user)