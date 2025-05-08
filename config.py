# config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "123456789"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "mysql+pymysql://usuario:123456789@localhost/ecotrack"
    SQLALCHEMY_TRACK_MODIFICATIONS = False