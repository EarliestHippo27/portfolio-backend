from datetime import timedelta
from dotenv import load_dotenv
import os
load_dotenv()

class Config:
  SECRET_KEY = os.environ["SECRET_KEY"]
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ECHO = False
  SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
  SESSION_COOKIE_SECURE=False
  SESSION_COOKIE_SAMESITE="Lax"
  SESSION_TYPE = "sqlalchemy"
  SESSION_PERMANENT = True
  PERMANENT_SESSION_LIFETIME=timedelta(days=3)