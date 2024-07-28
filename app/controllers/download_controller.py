# download_controller.py
import requests
import hashlib
import os
from flask import Blueprint, jsonify

download_bp = Blueprint('download_bp', __name__)

def file_checksum(filename):
    hash_func = hashlib.sha256()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

@download_bp.route('/download_scaler', methods=['GET'])
def download_scaler():
    scaler_filename = 'Scaler.pkl'
    scaler_url = 'http://example.com/path/to/Scaler.pkl'  # Replace with actual URL
    expected_checksum = 'expectedchecksumvalue'  # Replace with actual checksum

    if not os.path.exists(scaler_filename):
        response = requests.get(scaler_url)
        if response.status_code == 200:
            with open(scaler_filename, 'wb') as f:
                f.write(response.content)
            if file_checksum(scaler_filename) == expected_checksum:
                return jsonify({"message": "Scaler downloaded and verified successfully"}), 200
            else:
                os.remove(scaler_filename)
                return jsonify({"message": "Checksum verification failed"}), 500
        else:
            return jsonify({"message": "Failed to download scaler"}), 500
    else:
        if file_checksum(scaler_filename) == expected_checksum:
            return jsonify({"message": "Scaler already exists and is verified"}), 200
        else:
            os.remove(scaler_filename)
            return jsonify({"message": "Existing scaler file failed verification"}), 500
