from flask import jsonify
from app.models import Tag, db

def get_all_tags():
    tags = Tag.query.all()
    return jsonify([{'id': t.id, 'name': t.name} for t in tags])

def rename_tag(tag_id, request):
    data = request.get_json()
    new_name = data.get('name')

    tag = Tag.query.get(tag_id)
    if not tag:
        return jsonify({'error': 'Tag not found'}), 404

    tag.name = new_name
    db.session.commit()
    return jsonify({'message': 'Tag updated'})
