"""
Production Flask server for Face-Recon access control system.

This server provides API endpoints for user authentication and access control,
backed by SQLite database.
"""

import os
import sqlite3
import sys

# Ensure the parent directory is in the path for imports to work
# This allows the server to be run from various contexts
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import Flask, jsonify, request

from src.config import DATABASE_PATH

app = Flask(__name__)


def get_db_connection():
    """
    Create and return a database connection.

    Returns:
        sqlite3.Connection: Database connection with Row factory.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/access", methods=["POST"])
def check_access():
    """
    Check if a user has access to the system.

    Expected JSON payload:
        {
            "user": "username"
        }

    Returns:
        JSON response with access status:
        - {"access": true} if user exists
        - {"access": false} if user doesn't exist
        - {"error": "message"}, 400 for invalid requests
    """
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    user = data.get("user")
    if not user:
        return jsonify({"error": "User not provided"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (user,))
        user_row = cursor.fetchone()
        conn.close()

        if user_row:
            return jsonify({"access": True})
        return jsonify({"access": False})
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
