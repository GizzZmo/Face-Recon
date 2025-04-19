from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/access', methods=['POST'])
def check_access():
    data = request.json
    user = data["user"]
    
    # Simulert adgangssjekk
    if user in ["Jon", "Admin"]:
        return jsonify({"access": True})
    
    return jsonify({"access": False})

if __name__ == '__main__':
    app.run(debug=True)
