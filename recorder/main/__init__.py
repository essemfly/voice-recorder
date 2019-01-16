from flask import Blueprint

bp = Blueprint('main', __name__)

from recorder.main import routes, models