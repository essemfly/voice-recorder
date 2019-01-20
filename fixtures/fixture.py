import os.path
from flask import current_app
from recorder import db
from recorder.main.models import Script


def seed():
    basedir = os.path.dirname(os.path.abspath(__file__))

    for i in range(16):
        file = open(basedir + "/worlds_within_{}.txt".format(i+1), 'r')
        file_content = file.read()
        script = Script(id=i+1, text=file_content,
                        src_title='그들이사는세상 {}회'.format(str(i+1)), src_part=1)
        db.session.add(script)
        file.close()

    db.session.commit()
    return True
