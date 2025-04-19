async function requestAccess() {
    const response = await fetch('/access', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user: "Jon" })
    });
    const data = await response.json();
    alert(data.access ? "Adgang tillatt!" : "Ingen adgang!");
}
