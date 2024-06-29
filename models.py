from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    todolist = db.relationship("ToDoList", backref="user", lazy=True)
    contacts = db.relationship("ContactBook", backref="user", lazy=True)

    @staticmethod
    def create_password(password):
        hashed_password = generate_password_hash(
            password,
            method='pbkdf2:sha256',
            salt_length=8,
        )
        return hashed_password

    @staticmethod
    def check_password(email, password):
        user = db.session.query(User).filter_by(email=email).first()
        if user:
            return check_password_hash(user.password, str(password))
        return False


class ToDoList(db.Model):
    __tablename__ = "todolist"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey("user.id"))
    title = Column(String(120), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    priority = Column(String(50), nullable=False, default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)


class ContactBook(db.Model):
    __tablename__ = 'contact_book'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey("user.id"))
    name = Column(String(120), nullable=True)
    phone = Column(String(15), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)