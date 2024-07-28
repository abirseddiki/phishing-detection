from flask import Blueprint, request, jsonify
from app.entities.check import check_entity
from bson import ObjectId
check_bp = Blueprint('check_bp', __name__)

def serialize_check(check):
    check['_id'] = str(check['_id'])
    check['url_id'] = str(check['url_id'])
    return check
@check_bp.route('/checks', methods=['POST'])
def create_check():
    data = request.get_json()
    check_id = check_entity.create_check(data)
    return jsonify({"check_id": str(check_id)}), 201

@check_bp.route('/checks/<string:check_id>', methods=['GET'])
def get_check(check_id):
    check = check_entity.get_check(ObjectId(check_id))
    if check:
        return jsonify(serialize_check(check)), 200
    else:
        return jsonify({"error": "Check not found"}), 404

@check_bp.route('/checks/<string:check_id>', methods=['PUT'])
def update_check(check_id):
    data = request.get_json()
    check_entity.update_check(check_id, data)
    return jsonify({"message": "Check updated successfully"}), 200

@check_bp.route('/checks/<string:check_id>', methods=['DELETE'])
def delete_check(check_id):
    check_entity.delete_check(check_id)
    return jsonify({"message": "Check deleted successfully"}), 204
