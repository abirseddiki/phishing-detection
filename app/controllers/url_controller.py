from flask import Blueprint, request, jsonify
from app.entities.url import url_entity

url_bp = Blueprint('url_bp', __name__)

@url_bp.route('/urls', methods=['POST'])
def create_url():
    data = request.get_json()
    url_id = url_entity.add_url(data['client_id'], data['url'])
    return jsonify({"url_id": str(url_id)}), 201

@url_bp.route('/urls/<string:url_id>', methods=['GET'])
def get_url(url_id):
    url = url_entity.get_url(url_id)
    if url:
        url["_id"] = str(url["_id"])  # Convert ObjectId to string
        return jsonify(url), 200
    else:
        return jsonify({"error": "URL not found"}), 404

@url_bp.route('/urls/<string:url_id>', methods=['PUT'])
def update_url(url_id):
    data = request.get_json()
    update_result = url_entity.update_url(url_id, data)
    if update_result.matched_count > 0:
        return jsonify({"message": "URL updated successfully"}), 200
    else:
        return jsonify({"error": "URL not found"}), 404

@url_bp.route('/urls/<string:url_id>', methods=['DELETE'])
def delete_url(url_id):
    delete_result = url_entity.delete_url(url_id)
    if delete_result.deleted_count > 0:
        return jsonify({"message": "URL deleted successfully"}), 204
    else:
        return jsonify({"error": "URL not found"}), 404
