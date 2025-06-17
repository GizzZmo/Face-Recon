// Request access for a user (example: prompt for user name)
async function requestAccess() {
    const user = prompt("Enter your username:");
    if (!user) return;

    const response = await fetch("http://localhost:5000/access", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user })
    });
    const data = await response.json();
    alert(data.access ? "Access granted!" : "Access denied!");
}

// Fetch and display access stats from backend API
async function fetchStats() {
    const response = await fetch("http://localhost:5000/stats");
    if (!response.ok) {
        document.getElementById("stats").innerText = "Failed to load stats";
        return;
    }
    const stats = await response.json();
    let html = "<h2>Access Stats</h2><ul>";
    stats.forEach(([user, count]) => {
        html += `<li>${user}: ${count} accesses</li>`;
    });
    html += "</ul>";
    document.getElementById("stats").innerHTML = html;
}

window.onload = fetchStats;
