import os.path
from flask import render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from recorder import basedir
from recorder.main import bp
from recorder.main.models import Script


ALLOWED_EXTENSIONS = set(['wmv', 'mp3'])


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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/voice', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        print(request.files['audio'])
        if 'audio' not in request.files:
            return redirect(request.url)
        file = request.files['audio']
        print(file)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(
                basedir, current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main.index'))
