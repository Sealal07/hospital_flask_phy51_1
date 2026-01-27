import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
    SECRET_KEY = os.urandom(24)
    WTF_CSRF_ENABLED = True