from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User, db

from app.utils.mail import send_welcome_email

from app.utils.image_handler import ImageHandler

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.form

    if "image" not in request.files:
        return jsonify({"message": "Image file is required"}), 400
    

    image = request.files["image"]
    uploaded_file = ImageHandler.upload_to_cloudinary(image, "profile_pictures")

    if not uploaded_file:
        return jsonify({"message": "Image upload failed"}), 500

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(username=data["username"], email=data.get("email"), profilepic=uploaded_file["original_url"])
    user.create_password_hash(data["password"])
    user.set_gender(data["gender"].lower())
    user.set_role(data["role"].lower())
    user.set_status("active")
    db.session.add(user)
    db.session.commit()

    send_welcome_email(user)

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 409

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    email_address = data.get("email")
    new_password = data.get("new_password")

    user = User.query.filter_by(email=email_address).first()
    if not user:
        return jsonify({"message": "User not found"}), 407

    user.create_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password reset successfully"}), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return (
        jsonify({"username": user.username, "email": user.email, "role": user.role}),
        200,
    )

@auth_bp.route("/change-role", methods=["POST"])
@jwt_required()
def change_role():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_role = data.get("new_role")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.set_role(new_role)
    db.session.commit()
    return jsonify({"message": "Role updated successfully"}), 200