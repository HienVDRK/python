#~project_anm/database/accounts.py
from .db import db

class account_bank(db.Document):
    account_number = db.IntField(required=True, unique=True)
    balance = db.IntField(required=True)
    firstname = db.StringField(required=True)
    lastname = db.StringField(required=True)
    age = db.IntField(required=True)
    gender = db.StringField(required=True)
    address = db.StringField(required=True)
    employer = db.StringField(required=True)
    email = db.StringField(required=True)
    city = db.StringField(required=True)
    state = db.StringField(required=True)
    
        