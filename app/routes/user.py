from flask import Blueprint, request
from app.controllers.user import register_user, login_user

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    return register_user(request)

@user_bp.route('/login', methods=['POST'])
def login():
    return login_user(request)
