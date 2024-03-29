from recorder import db
from recorder.serializer import Serializer
from datetime import datetime


class Script(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    src_title = db.Column(db.String(64))
    src_part = db.Column(db.Integer)

    def __repr__(self):
        return '<Script {}>'.format(self.src_title + "-" + str(self.src_part))


class Voice(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128))
    sentence = db.Column(db.String(256))
    duration = db.Column(db.Interval)
    script_id = db.Column(db.Integer, db.ForeignKey('script.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Voice {}>'.format(str(self.id) + ":" + self.filename)

    def serialize(self):
        return Serializer.serialize(self)