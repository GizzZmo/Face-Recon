"""
Production Flask server for Face-Recon access control system.

This server provides API endpoints for user authentication, access control,
access logging, and statistics, backed by an SQLite database.
"""

import logging
import os
import sqlite3
import sys

# Ensure the parent directory is in the path for imports to work
# This allows the server to be run from various contexts
# Go up one level: backend/server.py -> backend -> project_root
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from flask import Flask, jsonify, request

from src.config import DATABASE_PATH

app = Flask(__name__)

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)

# SQL schema used to initialise the database on first run
_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    face_encoding BLOB,
    access_start TIME,
    access_end TIME,
    rfid_code TEXT DEFAULT NULL,
    nfc_tag TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS access_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_granted BOOLEAN,
    method TEXT DEFAULT 'face'
);
"""


def init_db() -> None:
    """
    Initialise the database, creating tables if they do not exist.

    The database file path is read from ``src.config.DATABASE_PATH``.
    The parent directory is created automatically when needed.
    """
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.executescript(_SCHEMA)
    conn.commit()
    conn.close()


def get_db_connection() -> sqlite3.Connection:
    """
    Create and return a database connection.

    Returns:
        sqlite3.Connection: Database connection with Row factory.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _log_access(user: str, granted: bool, method: str = "face") -> None:
    """
    Write an access event to the ``access_log`` table.

    Args:
        user: The username that attempted access.
        granted: Whether access was granted.
        method: Authentication method used (default: ``"face"``).
    """
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO access_log (user, access_granted, method) VALUES (?, ?, ?)",
            (user, granted, method),
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as exc:
        # Log to server-side output so administrators can investigate without
        # exposing internal details to API callers.
        _logger.error("Failed to write access log entry: %s", exc)


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------


@app.route("/access", methods=["POST"])
def check_access():
    """
    Check whether a user has access to the system.

    Expected JSON payload::

        {"user": "username"}

    Returns:
        JSON response:
        - ``{"access": true}``  – user exists and is allowed.
        - ``{"access": false}`` – user is not registered.
        - ``{"error": "..."}`` 400 – malformed request.
        - ``{"error": "..."}`` 500 – database error.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    user = data.get("user")
    if not user or not isinstance(user, str):
        return jsonify({"error": "User not provided"}), 400

    method = data.get("method", "face")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (user,))
        user_row = cursor.fetchone()
        granted = user_row is not None
    except sqlite3.Error as exc:
        _logger.error("Database error in check_access: %s", exc)
        return jsonify({"error": "A database error occurred"}), 500
    finally:
        conn.close()

    _log_access(user, granted, method)
    return jsonify({"access": granted})


@app.route("/stats", methods=["GET"])
def get_stats():
    """
    Return per-user access statistics.

    Returns:
        JSON list of ``[username, total_accesses, granted_accesses]`` tuples,
        ordered by total accesses descending.
    """
    conn = get_db_connection()
    try:
        rows = conn.execute("""
            SELECT user,
                   COUNT(*) AS total,
                   SUM(CASE WHEN access_granted THEN 1 ELSE 0 END) AS granted
            FROM access_log
            GROUP BY user
            ORDER BY total DESC
            """).fetchall()
        return jsonify([[row["user"], row["total"], row["granted"]] for row in rows])
    except sqlite3.Error as exc:
        _logger.error("Database error in get_stats: %s", exc)
        return jsonify({"error": "A database error occurred"}), 500
    finally:
        conn.close()


@app.route("/logs", methods=["GET"])
def get_logs():
    """
    Return the most recent access log entries.

    Query parameters:
        limit (int): Maximum number of entries to return (default 50, max 500).

    Returns:
        JSON list of log entry objects with keys:
        ``id``, ``user``, ``timestamp``, ``access_granted``, ``method``.
    """
    try:
        limit = min(int(request.args.get("limit", 50)), 500)
    except (ValueError, TypeError):
        limit = 50

    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT id, user, timestamp, access_granted, method "
            "FROM access_log ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return jsonify(
            [
                {
                    "id": row["id"],
                    "user": row["user"],
                    "timestamp": row["timestamp"],
                    "access_granted": bool(row["access_granted"]),
                    "method": row["method"],
                }
                for row in rows
            ]
        )
    except sqlite3.Error as exc:
        _logger.error("Database error in get_logs: %s", exc)
        return jsonify({"error": "A database error occurred"}), 500
    finally:
        conn.close()


@app.route("/users", methods=["GET"])
def list_users():
    """
    List all registered users.

    Returns:
        JSON list of user objects with keys: ``id``, ``name``,
        ``access_start``, ``access_end``, ``rfid_code``, ``nfc_tag``.
    """
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT id, name, access_start, access_end, rfid_code, nfc_tag FROM users"
        ).fetchall()
        return jsonify(
            [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "access_start": row["access_start"],
                    "access_end": row["access_end"],
                    "rfid_code": row["rfid_code"],
                    "nfc_tag": row["nfc_tag"],
                }
                for row in rows
            ]
        )
    except sqlite3.Error as exc:
        _logger.error("Database error in list_users: %s", exc)
        return jsonify({"error": "A database error occurred"}), 500
    finally:
        conn.close()


@app.route("/users", methods=["POST"])
def create_user():
    """
    Register a new user.

    Expected JSON payload::

        {
            "name": "username",
            "access_start": "08:00",  (optional)
            "access_end": "18:00",    (optional)
            "rfid_code": "AABB...",   (optional)
            "nfc_tag": "TAG01"        (optional)
        }

    Returns:
        - ``{"id": <new_id>, "name": "username"}`` 201 on success.
        - ``{"error": "..."}`` 400 / 409 / 500 on failure.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    name = data.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        return jsonify({"error": "Valid 'name' is required"}), 400

    name = name.strip()
    access_start = data.get("access_start")
    access_end = data.get("access_end")
    rfid_code = data.get("rfid_code")
    nfc_tag = data.get("nfc_tag")

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (name, access_start, access_end, rfid_code, nfc_tag) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, access_start, access_end, rfid_code, nfc_tag),
        )
        conn.commit()
        new_id = cursor.lastrowid
        return jsonify({"id": new_id, "name": name}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": f"User '{name}' already exists"}), 409
    except sqlite3.Error as exc:
        _logger.error("Database error in create_user: %s", exc)
        return jsonify({"error": "A database error occurred"}), 500
    finally:
        conn.close()


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    """
    Remove a user from the system.

    Args:
        user_id: The integer primary key of the user to remove.

    Returns:
        - ``{"deleted": true}`` 200 if the user was removed.
        - ``{"error": "User not found"}`` 404 if no such user exists.
        - ``{"error": "..."}`` 500 on database error.
    """
    conn = get_db_connection()
    try:
        cursor = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"deleted": True})
    except sqlite3.Error as exc:
        _logger.error("Database error in delete_user: %s", exc)
        return jsonify({"error": "A database error occurred"}), 500
    finally:
        conn.close()


@app.route("/health", methods=["GET"])
def health_check():
    """
    Simple health-check endpoint.

    Returns:
        ``{"status": "ok"}`` 200 always.
    """
    return jsonify({"status": "ok"})


# ---------------------------------------------------------------------------
# Application entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
