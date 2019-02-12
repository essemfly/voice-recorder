from flask_script import Manager
from flask_migrate import MigrateCommand
from recorder import create_app, db
from fixtures import fixture

app = create_app()
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed_first():
    fixture.add_worlds_within()


@manager.command
def seed_second():
    fixture.add_lyrics_2018_first()


manager.run()
