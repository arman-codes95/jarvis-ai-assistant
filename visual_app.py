from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = "jarvis_secret_key"

current_state = "idle"
current_energy = 0

USERS_FILE = "data/users.json"


# ----------------------
# LOAD USERS
# ----------------------
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}


# ----------------------
# LOGIN PAGE
# ----------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        users = load_users()

        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["title"] = users[username]["title"]
            return redirect(url_for("index"))

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


# ----------------------
# LOGOUT
# ----------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ----------------------
# MAIN UI
# ----------------------
@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template(
        "visual.html",
        username=session["user"],
        title=session["title"]
    )


# ----------------------
# STATE API
# ----------------------
@app.route("/state")
def state():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "state": current_state,
        "energy": current_energy
    })


# ----------------------
# UPDATE STATE
# ----------------------
@app.route("/update_state", methods=["POST"])
def update_state():
    global current_state, current_energy
    data = request.json
    current_state = data.get("state", "idle")
    current_energy = data.get("energy", 0)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)
    
    
@app.route("/user")
def get_user():

    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "username": session["user"],
        "title": session["title"]
    })