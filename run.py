from flask_script import Manager
from flask_migrate import MigrateCommand
from recorder import create_app, db
from fixtures import fixture

app = create_app()
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    fixture.seed()


manager.run()
