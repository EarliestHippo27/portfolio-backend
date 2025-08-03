from flask import Flask, request, Response, jsonify, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_cors import CORS
from flask_login import current_user, login_user, logout_user, LoginManager
from os import path
from .models import db, User
from .config import Config
from.res import res


def create_database():
    db.create_all()

DB_NAME = "database.db"

app = Flask(__name__)
app.config.from_object(Config)
app.config["SESSION_SQLALCHEMY"] = db

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
Session(app)
CORS(app, supports_credentials=True)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

with app.app_context():
    create_database()


@login_manager.user_loader
def load_user(user_id: int):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":

        data = request.get_json()
        email = data["email"]
        password = data["password"]

        if User.query.filter_by(email=email).first() is not None:
            # If email is already registered
            return res(409)

        newPassword = bcrypt.generate_password_hash(password)

        newUser = User(email=email, password=newPassword)
        db.session.add(newUser)
        db.session.commit()
    return res(201)


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        logout_user()

        data = request.get_json()
        email = data["email"]
        password = data["password"]

        user: User = User.query.filter_by(email=email).first()

        if user is None:
            # If email is not registered
            return res(401)

        if not bcrypt.check_password_hash(user.password, password):
            return res(401)

        # Give user session stuff to say logged in
        login_user(user)
    return res(200)


@app.route("/auth", methods=["GET"])
def auth():
    if current_user.is_authenticated:
        return res(200, data={"id": current_user.id}, message="Secure Page")
    return res(401, message="Not Logged In/Session Expired")


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return res(200,message="Logged Out")