from flask import Blueprint, request
from app.controllers.tag import get_all_tags, rename_tag

tag_bp = Blueprint('tags', __name__)

@tag_bp.route('/listtag', methods=['GET'])
def list_tags():
    return get_all_tags()

@tag_bp.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    return rename_tag(tag_id, request)
