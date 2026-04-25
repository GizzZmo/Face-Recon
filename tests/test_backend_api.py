"""
Integration tests for the Face-Recon Flask backend server.

These tests use Flask's built-in test client so no running server is
required.  A temporary SQLite database is used for each test session.
"""

import os
import sys

import pytest

# Ensure project root is on the path so backend.server can import src.config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    """
    Provide a Flask test client backed by a temporary SQLite database.

    The database is created fresh for this test module and torn down
    afterwards.
    """
    db_path = str(tmp_path_factory.mktemp("db") / "test_face_recon.db")

    # Monkey-patch DATABASE_PATH before importing the server
    import src.config as cfg

    original_db_path = cfg.DATABASE_PATH
    cfg.DATABASE_PATH = db_path

    # Import server *after* patching
    from backend.server import app, init_db

    init_db()
    app.config["TESTING"] = True

    with app.test_client() as c:
        yield c

    # Restore original path
    cfg.DATABASE_PATH = original_db_path


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------


class TestHealth:
    def test_health_returns_ok(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.get_json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# /users
# ---------------------------------------------------------------------------


class TestUsers:
    def test_list_users_empty(self, client):
        res = client.get("/users")
        assert res.status_code == 200
        assert res.get_json() == []

    def test_create_user(self, client):
        res = client.post("/users", json={"name": "alice"})
        assert res.status_code == 201
        data = res.get_json()
        assert data["name"] == "alice"
        assert "id" in data

    def test_create_user_duplicate(self, client):
        client.post("/users", json={"name": "bob"})
        res = client.post("/users", json={"name": "bob"})
        assert res.status_code == 409
        assert "already exists" in res.get_json()["error"]

    def test_create_user_missing_name(self, client):
        res = client.post("/users", json={})
        assert res.status_code == 400

    def test_create_user_no_body(self, client):
        res = client.post("/users", data="not json", content_type="text/plain")
        # Flask returns 415 (Unsupported Media Type) when Content-Type is not JSON
        assert res.status_code in (400, 415)

    def test_list_users_contains_created(self, client):
        client.post("/users", json={"name": "charlie"})
        res = client.get("/users")
        names = [u["name"] for u in res.get_json()]
        assert "alice" in names
        assert "charlie" in names

    def test_delete_user(self, client):
        res_create = client.post("/users", json={"name": "delete_me"})
        uid = res_create.get_json()["id"]
        res_delete = client.delete(f"/users/{uid}")
        assert res_delete.status_code == 200
        assert res_delete.get_json()["deleted"] is True

    def test_delete_nonexistent_user(self, client):
        res = client.delete("/users/99999")
        assert res.status_code == 404


# ---------------------------------------------------------------------------
# /access
# ---------------------------------------------------------------------------


class TestAccess:
    def test_access_granted_for_registered_user(self, client):
        client.post("/users", json={"name": "granted_user"})
        res = client.post("/access", json={"user": "granted_user"})
        assert res.status_code == 200
        assert res.get_json()["access"] is True

    def test_access_denied_for_unknown_user(self, client):
        res = client.post("/access", json={"user": "unknown_xyz"})
        assert res.status_code == 200
        assert res.get_json()["access"] is False

    def test_access_no_body(self, client):
        res = client.post("/access", data="", content_type="application/json")
        assert res.status_code == 400

    def test_access_missing_user_field(self, client):
        res = client.post("/access", json={"method": "face"})
        assert res.status_code == 400

    def test_access_with_method(self, client):
        client.post("/users", json={"name": "nfc_user"})
        res = client.post("/access", json={"user": "nfc_user", "method": "nfc"})
        assert res.status_code == 200
        assert res.get_json()["access"] is True


# ---------------------------------------------------------------------------
# /logs
# ---------------------------------------------------------------------------


class TestLogs:
    def test_logs_returns_list(self, client):
        res = client.get("/logs")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_logs_records_access_attempts(self, client):
        client.post("/users", json={"name": "log_test_user"})
        client.post("/access", json={"user": "log_test_user"})
        client.post("/access", json={"user": "nonexistent_log_user"})

        logs = client.get("/logs").get_json()
        users_logged = [entry["user"] for entry in logs]
        assert "log_test_user" in users_logged
        assert "nonexistent_log_user" in users_logged

    def test_logs_entry_structure(self, client):
        logs = client.get("/logs").get_json()
        assert len(logs) > 0
        entry = logs[0]
        assert "id" in entry
        assert "user" in entry
        assert "timestamp" in entry
        assert "access_granted" in entry
        assert "method" in entry

    def test_logs_limit_parameter(self, client):
        res = client.get("/logs?limit=2")
        assert res.status_code == 200
        assert len(res.get_json()) <= 2

    def test_logs_default_method_is_face(self, client):
        client.post("/users", json={"name": "method_default_user"})
        client.post("/access", json={"user": "method_default_user"})
        logs = client.get("/logs?limit=1").get_json()
        assert logs[0]["method"] == "face"

    def test_logs_custom_method_recorded(self, client):
        client.post("/users", json={"name": "method_custom_user"})
        client.post("/access", json={"user": "method_custom_user", "method": "voice"})
        logs = client.get("/logs?limit=1").get_json()
        assert logs[0]["method"] == "voice"


# ---------------------------------------------------------------------------
# /stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_stats_returns_list(self, client):
        res = client.get("/stats")
        assert res.status_code == 200
        assert isinstance(res.get_json(), list)

    def test_stats_entry_structure(self, client):
        stats = client.get("/stats").get_json()
        for entry in stats:
            assert len(entry) == 3  # [user, total, granted]
            user, total, granted = entry
            assert isinstance(user, str)
            assert isinstance(total, int)
            assert isinstance(granted, int)
            assert total >= granted >= 0
