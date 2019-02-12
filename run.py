from flask_script import Manager
from flask_migrate import MigrateCommand
from fixtures import fixture
from recorder import create_app, db
from recorder.main.models import Voice
from recorder.auth.models import User
import json

app = create_app()
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed_first():
    fixture.add_worlds_within()


@manager.command
def seed_second():
    fixture.add_lyrics_2018_first()


@manager.command
def generate_json(username):
    user = User.query.filter_by(username=username).first()
    records = Voice.query.filter_by(user_id=user.id).all()

    data = {}

    for record in records:
        key_name = "./datasets/%s/audio/%s" % (user.username, record.filename)
        data[key_name] = record.sentence

    with open('./voice_data/%s/alignment.json' % (user.username), 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)

    return "Finished records: %s" % (str(len(records)))

manager.run()
