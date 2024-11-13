from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin
from api import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    total_likes = db.Column(db.Integer, default=0)
    total_loves = db.Column(db.Integer, default=0)
    total_dislikes = db.Column(db.Integer, default=0)
    daily_hearts = db.Column(db.Integer, default=10)
    last_reset_date = db.Column(db.Date, default=datetime.utcnow)

    photos = db.relationship('Photo', backref='user', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def reset_daily_hearts(self):
        if self.last_reset_date < datetime.utcnow().date():
            self.daily_hearts = 10
            self.last_reset_date = datetime.utcnow().date()
            db.session.commit()

class Photo(db.Model):
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.Column(JSON, default=[])
    likes = db.Column(db.Integer, default=0)
    loves = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
