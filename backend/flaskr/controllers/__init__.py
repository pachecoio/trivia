from flask import jsonify
from app import app


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": True, "message": "Resourse not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": True, "message": "Server error"}), 500
