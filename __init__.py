from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "a234drwer"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:Mwerxz23@localhost/Infinity"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    db.init_app(app)
    Session(app)

    from .views import some_blueprint
    from .auth import auth

    app.register_blueprint(some_blueprint, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    from .models import Users

    with app.app_context():
        db.create_all()
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))
    

    return app
