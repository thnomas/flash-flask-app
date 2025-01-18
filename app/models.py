from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from dataclasses import dataclass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    

@dataclass
class User(db.Model, UserMixin):
    id: int
    email: str
    username:str
    password:str
    image_file:str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    decks = db.relationship('Deck', backref='created_by', lazy=True)
    cards = db.relationship('Card', backref='author', lazy=True)

    def __repr__(self):
        return f"User ('{self.username}', '{self.email}')"

@dataclass
class Deck(db.Model):
    id: int
    title: str
    description:str
    created_at:datetime
    user_id:int

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cards = db.relationship('Card', backref='deck', lazy=True)

    def __repr__(self):
        return f"Deck ('{self.title}', '{self.created_at}')"

@dataclass
class Card(db.Model):
    id: int
    front: str
    back:str
    created_at:datetime
    user_id:int
    deck_id:int

    id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'), nullable=False)

    def __repr__(self):
        return f"Card ('{self.front}', '{self.back}')"