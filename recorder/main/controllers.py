from recorder.main import bp
from flask import render_template
from flask_login import login_required, current_user
from recorder.main.models import Script


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    scripts = Script.query.all()
    return render_template('main/index.html', user=current_user, scripts=scripts)


@bp.route('/scripts/<int:script_id>')
def record(script_id):
    script = Script.query.get(script_id)
    return render_template('/main/record.html', script=script)