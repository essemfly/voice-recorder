# -*- coding: utf-8 -*-

import os.path
import datetime
from flask import render_template, request, current_app, redirect, url_for, json
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from recorder import basedir, db
from recorder.main import bp
from recorder.main.models import Script, Voice
from recorder.auth.models import User
from functools import reduce

ALLOWED_EXTENSIONS = set(['wav', 'mp3'])


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    scripts = Script.query.all()
    return render_template('main/index.html', user=current_user, scripts=scripts)


@bp.route('/scripts/<int:script_id>')
def record(script_id):
    script = Script.query.get(script_id)
    return render_template('/main/record.html', script=script, user=current_user)

@bp.route('/scripts/seq/<int:script_id>')
def record_seq(script_id):
    script = Script.query.get(script_id)
    return render_template('/main/record_seq.html', script=script, user=current_user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/voices/<int:user_id>')
def user(user_id):
    voices = Voice.query.filter_by(user_id=user_id).all()
    voices_json = []
    seconds = 0

    for voice in voices:
        print('hoit', voice.duration)
        voice_temp = {}
        voice_temp["duration"] = voice.duration.total_seconds()
        voice_temp["sentence"] = voice.sentence
        voice_temp["filename"] = voice.filename
        voice_temp["created_at"] = voice.created_at.replace(microsecond=0).isoformat()
        voices_json.append(voice_temp)
        seconds += voice.duration.total_seconds()
    
    print(seconds)
    return render_template('/main/voice.html', voices=json.dumps(voices_json, ensure_ascii=False), total_seconds=seconds)

@bp.route('/voice/<int:user_id>/<int:script_id>', methods=['GET', 'POST'])
def upload_file(user_id, script_id):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'audio' not in request.files:
            return redirect(request.url)
        file = request.files['audio']
        sentence = request.form['sentence']
        duration = request.form['duration']
        filename = request.form['filename']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            user = User.query.get(user_id)
            file.save(os.path.join(
                basedir, current_app.config['UPLOAD_FOLDER'] + "/" + user.username, filename))
            voice = Voice(filename = filename, sentence= sentence, duration=duration, script_id=script_id, user_id=user_id)
            db.session.add(voice)
            db.session.commit()
            return redirect(url_for('main.index'))
