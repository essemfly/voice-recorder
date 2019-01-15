from flask import Flask
from .models import db, login_manager

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

from recorder.errors import bp as errors_bp
app.register_blueprint(errors_bp)

db.init_app(app)
login_manager.init_app(app)

from . import routes, models