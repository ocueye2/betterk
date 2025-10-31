import sqlite3
from flask import Blueprint, request, g, redirect, url_for, render_template
from flask_login import login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# ---------- Database helpers ----------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("users.db")
        g.db.row_factory = sqlite3.Row
    return g.db

@auth_bp.teardown_app_request
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    db.commit()

# ---------- User model ----------
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def load_user_by_id(user_id):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if user:
        return User(user["id"], user["username"], user["password"])
    return None

# ---------- Routes ----------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hash_pw = generate_password_hash(password)

        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_pw))
            db.commit()
        except sqlite3.IntegrityError:
            return "Username already taken"
        return "Registered!"
    
    return '''
        <form method="post">
            <input name="username" placeholder="username">
            <input name="password" type="password" placeholder="password">
            <input type="submit" value="Register">
        </form>
    '''

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user["password"], password):
            login_user(User(user["id"], user["username"], user["password"]))
            return redirect(url_for("protected"))
        return render_template("auth/login.html", error="Invalid credentials")

    return render_template("auth/login.html", error="")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"
