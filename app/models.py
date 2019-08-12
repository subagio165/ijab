from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin ):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isi = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.isi}', '{self.tanggal}')"

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aksi = db.Column(db.Text, nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Text, nullable=False)
    user_ip = db.Column(db.Text, nullable=False)