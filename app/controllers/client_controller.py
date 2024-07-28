from flask import Blueprint, request, jsonify
from app.entities.client import client_entity  # Make sure client_entity is imported

client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/clients/<string:client_id>', methods=['GET'])
def get_client(client_id):
    client = client_entity.get_client(client_id)
    if client:
        client["_id"] = str(client["_id"])  # Convert ObjectId to string
        return jsonify(client), 200
    else:
        return jsonify({"error": "Client not found"}), 404

@client_bp.route('/clients/<string:client_id>', methods=['PUT'])
def update_client(client_id):
    data = request.get_json()
    update_result = client_entity.update_client(client_id, data)
    if update_result.matched_count > 0:
        return jsonify({"message": "Client updated successfully"}), 200
    else:
        return jsonify({"error": "Client not found"}), 404

@client_bp.route('/clients/<string:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client_entity.deactivate_client(client_id)
    return jsonify({"message": "Client deactivated successfully"}), 204