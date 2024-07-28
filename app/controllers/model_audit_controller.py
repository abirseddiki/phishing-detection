from flask import Blueprint, request, jsonify
from app.entities.model_audit import model_audit_entity
from bson import ObjectId

model_audit_bp = Blueprint('model_audit_bp', __name__)

def serialize_model_audit(model_audit):
    model_audit['_id'] = str(model_audit['_id'])
    return model_audit

@model_audit_bp.route('/model_audits', methods=['POST'])
def create_model_audit():
    data = request.get_json()
    model_id = model_audit_entity.create_model_audit(data)
    return jsonify({"model_id": str(model_id)}), 201

@model_audit_bp.route('/model_audits/<string:model_id>', methods=['GET'])
def get_model_audit(model_id):
    model_audit = model_audit_entity.get_model_audit(ObjectId(model_id))
    if model_audit:
        return jsonify(serialize_model_audit(model_audit)), 200
    else:
        return jsonify({"error": "Model audit not found"}), 404

@model_audit_bp.route('/model_audits/<string:model_id>', methods=['PUT'])
def update_model_audit(model_id):
    data = request.get_json()
    updated = model_audit_entity.update_model_audit(ObjectId(model_id), data)
    if updated.matched_count:
        return jsonify({"message": "Model audit updated successfully"}), 200
    else:
        return jsonify({"error": "Model audit not found"}), 404

@model_audit_bp.route('/model_audits/<string:model_id>', methods=['DELETE'])
def delete_model_audit(model_id):
    deleted = model_audit_entity.delete_model_audit(ObjectId(model_id))
    if deleted.deleted_count:
        return jsonify({"message": "Model audit deleted successfully"}), 204
    else:
        return jsonify({"error": "Model audit not found"}), 404
