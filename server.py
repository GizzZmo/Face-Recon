"""
Simple Flask server for basic access control demonstration.
Note: This is a basic demo. Use backend/server.py for production.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/access", methods=["POST"])
def check_access():
    """Check if user has access based on simple whitelist."""
    data = request.json
    if not data or "user" not in data:
        return jsonify({"error": "User not provided"}), 400

    user = data["user"]

    # Simple access check (for demonstration only)
    if user in ["Jon", "Admin"]:
        return jsonify({"access": True})

    return jsonify({"access": False})


if __name__ == "__main__":
    app.run(debug=True)
