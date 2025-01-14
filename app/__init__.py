from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_assets import Environment, Bundle

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "Please log in to access this page."


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    print(app.config["SQLALCHEMY_DATABASE_URI"])
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    assets = Environment(app)
    scss = Bundle("scss/style.scss", filters="pyscss", output="css/style.css")
    assets.register("scss_all", scss)
    # print(db.engine)
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.pack import bp as pack_bp

    app.register_blueprint(pack_bp, url_prefix="/pack")
    return app


from app import models  # noqa: E402, F401
