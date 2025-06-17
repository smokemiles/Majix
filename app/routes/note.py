from flask import Blueprint, jsonify
from app.controllers.note import create_note, get_all_notes, get_note_by_id, update_note, delete_note
from flask_jwt_extended import jwt_required

note_bp = Blueprint('notes', __name__)

@note_bp.route('/createnote', methods=['POST'])
@jwt_required()
def create():
    return create_note()

@note_bp.route('/listnote', methods=['GET'])  
def list_notes():
    return get_all_notes()

@note_bp.route('/<int:note_id>', methods=['GET'])
def get_note(note_id):
    return get_note_by_id(note_id)

@note_bp.route('/<int:note_id>', methods=['PUT'])
def update(note_id):
    return update_note(note_id)

@note_bp.route('/<int:note_id>', methods=['DELETE'])
def delete(note_id):
    return delete_note(note_id)
