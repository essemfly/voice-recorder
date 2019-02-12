import os.path
from flask import current_app
from recorder import db
from recorder.main.models import Script


def add_worlds_within():
    basedir = os.path.dirname(os.path.abspath(__file__))

    for i in range(16):
        file = open(
            basedir + "/worlds_within/worlds_within_{}.txt".format(i+1), 'r')
        file_content = file.read()
        script = Script(id=i+1, text=file_content,
                        src_title='그들이사는세상 {}회'.format(str(i+1)), src_part=1)
        db.session.add(script)
        file.close()

    db.session.commit()
    return 'Success'


def add_lyrics_2018_first():
    path = os.path.dirname(os.path.abspath(__file__)) + '/lyrics2018/'
    start_id = 17

    filename = ["오늘의 루프탑", "마키코 언니", "봉이", "비밀이 사는 아파트", "치킨 보이",
                "애도의 방식", "플랫폼", "볼트", "피에카르스키를 찾아서", "그 여자의 거짓말", "어느 삼거리에서"]
    for filename in os.listdir(path):
        file = open(path + filename, 'r')
        file_content = file.read()
        script = Script(id=start_id, text=file_content,
                        src_title=filename[0], src_part=1)
        start_id += 1
        db.session.add(script)
        filename.pop(0)
        file.close()

    db.session.commit()
