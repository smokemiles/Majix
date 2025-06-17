from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

def register_user(request):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 400

    hashed_pw = generate_password_hash(password)
    new_user = User(email=email, password_hash=hashed_pw)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def login_user(request):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Placeholder for session or JWT
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200
