import sqlite3

from flask import Flask, jsonify, request

from src.config import DATABASE_PATH

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/access", methods=["POST"])
def check_access():
    data = request.json
    user = data.get("user")
    if not user:
        return jsonify({"error": "User not provided"}), 400

    # Example: Just check if user exists (expand logic for your needs)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ?", (user,))
    user_row = cursor.fetchone()
    conn.close()

    if user_row:
        return jsonify({"access": True})
    return jsonify({"access": False})


if __name__ == "__main__":
    app.run(debug=True)
