from flask import jsonify, request
from app.models import db, Note, Tag
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.image_handler import ImageHandler


def create_note():
    data = request.form

    if "image" not in request.files:
        return jsonify({"message": "Image file is required"}), 400

    image = request.files["image"]
    uploaded_file = ImageHandler.upload_to_cloudinary(image, "note_images")

    if not uploaded_file:
        return jsonify({"message": "Image upload failed"}), 500

    image = data.get(notepic=uploaded_file["original_url"])
    title = data.get('title')
    content = data.get('content', '')
    tags = data.get('tags', [])
    # user_id = data.get('user_id')  # TODO: replace with actual authenticated user ID
    user_id = get_jwt_identity()  # Get the authenticated user's ID

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    note = Note(title=title, content=content, user_id=user_id)  # TODO: replace with actual authenticated user ID

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        note.tags.append(tag)

    try:
        db.session.add(note)
        db.session.commit()
        return jsonify({'message': 'Note created', 'note_id': note.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

def get_all_notes():
    try:
        notes = Note.query.all()
        notes_data = []
        for note in notes:
            notes_data.append({
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'tags': [tag.name for tag in note.tags],
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat()
            })
        return jsonify(notes_data), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500

def get_note_by_id(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    note_data = {
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'tags': [tag.name for tag in note.tags],
        'created_at': note.created_at.isoformat(),
        'updated_at': note.updated_at.isoformat()
    }
    return jsonify(note_data), 200


def update_note(note_id):
    data = request.get_json()
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    title = data.get('title')
    content = data.get('content', '')
    tags = data.get('tags', [])

    if title:
        note.title = title
    if content:
        note.content = content

    note.tags.clear()
    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.session.add(tag)
        note.tags.append(tag)

    try:
        db.session.commit()
        return jsonify({'message': 'Note updated'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def delete_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        return jsonify({'error': 'Note not found'}), 404

    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
