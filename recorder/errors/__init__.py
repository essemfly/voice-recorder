from flask import Blueprint

bp = Blueprint('errors', __name__)

from recorder.errors import handlers