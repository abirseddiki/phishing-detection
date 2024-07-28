from flask import Blueprint, request, jsonify
from app.entities.feedback import feedback_entity
from bson import ObjectId

feedback_bp = Blueprint('feedback_bp', __name__)

def serialize_feedback(feedback):
    feedback['_id'] = str(feedback['_id'])
    return feedback

@feedback_bp.route('/feedbacks', methods=['POST'])
def create_feedback():
    data = request.get_json()
    feedback_id = feedback_entity.create_feedback(data)
    return jsonify({"feedback_id": str(feedback_id)}), 201

@feedback_bp.route('/feedbacks/<string:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    feedback = feedback_entity.get_feedback(ObjectId(feedback_id))
    if feedback:
        return jsonify(serialize_feedback(feedback)), 200
    else:
        return jsonify({"error": "Feedback not found"}), 404

@feedback_bp.route('/feedbacks/<string:feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    data = request.get_json()
    updated = feedback_entity.update_feedback(ObjectId(feedback_id), data)
    if updated.matched_count:
        return jsonify({"message": "Feedback updated successfully"}), 200
    else:
        return jsonify({"error": "Feedback not found"}), 404

@feedback_bp.route('/feedbacks/<string:feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    deleted = feedback_entity.delete_feedback(ObjectId(feedback_id))
    if deleted.deleted_count:
        return jsonify({"message": "Feedback deleted successfully"}), 204
    else:
        return jsonify({"error": "Feedback not found"}), 404
