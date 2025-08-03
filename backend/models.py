from flask import Flask
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
  id: Mapped[int] = mapped_column(primary_key=True, unique=True)
  email: Mapped[str] = mapped_column(String(30), unique=True)
  password: Mapped[str] = mapped_column(String(60))               # Password is hashed server side and this hash is stored here
                                                                  # Assumes hashed with Bcrypt which generates a 60 byte long bytes