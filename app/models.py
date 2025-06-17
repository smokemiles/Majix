from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(64), nullable=True, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    gender = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), nullable=True)
    profilepic = db.Column(db.String(255), nullable=True)



    def create_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

    def set_gender(self, new_gender):
        allowed = ["male", "female", "other"]
        if new_gender not in allowed:
            raise ValueError("Invalid gender")
        self.gender = new_gender

    def set_role(self, new_role):
        allowed = ["admin", "customer", "other"]
        if new_role not in allowed:
            raise ValueError("Invalid role")
        self.role = new_role

    def set_status(self, new_status):
        allowed = ["active", "inactive", "banned"]
        if new_status not in allowed:
            raise ValueError("Invalid role")
        self.status = new_status

    def to_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "gender": self.gender,
            "role": self.role,
            "status": self.status,
            "profilepic": self.profilepic
        }

    # notes = db.relationship('Note', backref='user', lazy=True, cascade="all, delete-orphan")
    # tags = db.relationship('Tag', backref='user', lazy=True, cascade="all, delete-orphan")

# --- Note Model ---
class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow)
    notepic = db.Column(db.String(255), nullable=True)


# --- Tag Model ---
class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'name', name='uq_user_tagname'),)

