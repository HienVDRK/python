#~project_anm/database/users.py
from .db import db

class User(db.Document):
    email = db.StringField(required=True, unique=True)
    username = db.StringField(required=True)
    password = db.StringField(required=True, min_length=6)
    role = db.StringField(required=True)
