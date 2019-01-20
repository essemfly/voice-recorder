import os.path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
login.login_view = 'auth.login'


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from recorder.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from recorder.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from recorder.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
