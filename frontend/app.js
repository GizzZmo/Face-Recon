const API_BASE = "http://localhost:5000";

// ---------------------------------------------------------------------------
// Health check
// ---------------------------------------------------------------------------

async function checkHealth() {
    const badge = document.getElementById("health-badge");
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            badge.textContent = "Server Online";
            badge.className = "badge badge-ok";
        } else {
            throw new Error("Non-OK response");
        }
    } catch {
        badge.textContent = "Server Offline";
        badge.className = "badge badge-error";
    }
}

// ---------------------------------------------------------------------------
// Access request
// ---------------------------------------------------------------------------

async function requestAccess() {
    const user = document.getElementById("username-input").value.trim();
    const method = document.getElementById("method-select").value;
    const resultBox = document.getElementById("access-result");

    if (!user) {
        showResult(resultBox, "Please enter a username.", "warn");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/access`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user, method }),
        });
        const data = await res.json();
        if (data.error) {
            showResult(resultBox, `Error: ${data.error}`, "error");
        } else {
            showResult(
                resultBox,
                data.access ? `✅ Access GRANTED for "${user}"` : `❌ Access DENIED for "${user}"`,
                data.access ? "ok" : "denied"
            );
        }
        // Refresh logs after an access attempt
        fetchLogs();
        fetchStats();
    } catch (err) {
        showResult(resultBox, `Network error: ${err.message}`, "error");
    }
}

// ---------------------------------------------------------------------------
// Statistics
// ---------------------------------------------------------------------------

async function fetchStats() {
    const container = document.getElementById("stats-container");
    container.innerHTML = "<p class='muted'>Loading…</p>";
    try {
        const res = await fetch(`${API_BASE}/stats`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const stats = await res.json();

        if (stats.length === 0) {
            container.innerHTML = "<p class='muted'>No access data yet.</p>";
            return;
        }

        let html = "<table><thead><tr><th>User</th><th>Total</th><th>Granted</th><th>Denied</th></tr></thead><tbody>";
        stats.forEach(([user, total, granted]) => {
            const denied = total - granted;
            html += `<tr>
                <td>${escapeHtml(user)}</td>
                <td>${total}</td>
                <td class="text-ok">${granted}</td>
                <td class="text-denied">${denied}</td>
            </tr>`;
        });
        html += "</tbody></table>";
        container.innerHTML = html;
    } catch (err) {
        container.innerHTML = `<p class='error'>Failed to load stats: ${err.message}</p>`;
    }
}

// ---------------------------------------------------------------------------
// Access logs
// ---------------------------------------------------------------------------

async function fetchLogs() {
    const limit = document.getElementById("log-limit").value;
    const container = document.getElementById("logs-container");
    container.innerHTML = "<p class='muted'>Loading…</p>";
    try {
        const res = await fetch(`${API_BASE}/logs?limit=${limit}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const logs = await res.json();

        if (logs.length === 0) {
            container.innerHTML = "<p class='muted'>No log entries yet.</p>";
            return;
        }

        let html = "<table><thead><tr><th>#</th><th>User</th><th>Time</th><th>Method</th><th>Result</th></tr></thead><tbody>";
        logs.forEach(entry => {
            const statusClass = entry.access_granted ? "text-ok" : "text-denied";
            const statusText = entry.access_granted ? "✅ Granted" : "❌ Denied";
            html += `<tr>
                <td>${entry.id}</td>
                <td>${escapeHtml(entry.user)}</td>
                <td>${escapeHtml(entry.timestamp)}</td>
                <td>${escapeHtml(entry.method)}</td>
                <td class="${statusClass}">${statusText}</td>
            </tr>`;
        });
        html += "</tbody></table>";
        container.innerHTML = html;
    } catch (err) {
        container.innerHTML = `<p class='error'>Failed to load logs: ${err.message}</p>`;
    }
}

// ---------------------------------------------------------------------------
// User management
// ---------------------------------------------------------------------------

async function fetchUsers() {
    const container = document.getElementById("users-container");
    container.innerHTML = "<p class='muted'>Loading…</p>";
    try {
        const res = await fetch(`${API_BASE}/users`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const users = await res.json();

        if (users.length === 0) {
            container.innerHTML = "<p class='muted'>No users registered yet.</p>";
            return;
        }

        const ul = document.createElement("ul");
        ul.className = "user-list";
        users.forEach(u => {
            const li = document.createElement("li");

            const nameSpan = document.createElement("span");
            nameSpan.textContent = u.name;

            const btn = document.createElement("button");
            btn.className = "btn-danger";
            btn.textContent = "Remove";
            btn.addEventListener("click", () => deleteUser(u.id, u.name));

            li.appendChild(nameSpan);
            li.appendChild(btn);
            ul.appendChild(li);
        });
        container.innerHTML = "";
        container.appendChild(ul);
    } catch (err) {
        container.innerHTML = `<p class='error'>Failed to load users: ${err.message}</p>`;
    }
}

async function addUser() {
    const input = document.getElementById("new-username");
    const name = input.value.trim();
    if (!name) return;

    try {
        const res = await fetch(`${API_BASE}/users`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name }),
        });
        const data = await res.json();
        if (res.status === 201) {
            input.value = "";
            fetchUsers();
        } else {
            alert(data.error || "Failed to add user.");
        }
    } catch (err) {
        alert(`Network error: ${err.message}`);
    }
}

async function deleteUser(userId, name) {
    if (!confirm(`Remove user "${name}"?`)) return;
    try {
        const res = await fetch(`${API_BASE}/users/${userId}`, { method: "DELETE" });
        const data = await res.json();
        if (data.deleted) {
            fetchUsers();
            fetchStats();
        } else {
            alert(data.error || "Failed to remove user.");
        }
    } catch (err) {
        alert(`Network error: ${err.message}`);
    }
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function showResult(element, message, type) {
    element.textContent = message;
    element.className = `result-box result-${type}`;
}

function escapeHtml(str) {
    if (str == null) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}

// ---------------------------------------------------------------------------
// Initialise on page load
// ---------------------------------------------------------------------------

const REFRESH_INTERVAL_MS = 30000;
let _refreshTimer = null;

function scheduleRefresh() {
    if (_refreshTimer !== null) return;
    _refreshTimer = setTimeout(async () => {
        _refreshTimer = null;
        if (document.visibilityState !== "hidden") {
            checkHealth();
            fetchStats();
            fetchLogs();
        }
        scheduleRefresh();
    }, REFRESH_INTERVAL_MS);
}

window.onload = function () {
    checkHealth();
    fetchStats();
    fetchLogs();
    fetchUsers();
    scheduleRefresh();

    // Pause auto-refresh when the tab is hidden, resume when visible
    document.addEventListener("visibilitychange", () => {
        if (document.visibilityState === "visible") {
            // Immediately refresh after becoming visible again
            checkHealth();
            fetchStats();
            fetchLogs();
            scheduleRefresh();
        }
    });
};

