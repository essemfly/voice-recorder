from flask import Blueprint

bp = Blueprint('auth', __name__)

from recorder.auth import routes