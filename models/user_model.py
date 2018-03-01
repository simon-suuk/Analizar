from models.base_model import *
from peewee import CharField, BooleanField, TextField, DateTimeField
from flask_login import UserMixin

from datetime import datetime


class UserModel(BaseModel):
    name = TextField(45)
    email = TextField(45)
    password = TextField(45)
    company_name = TextField(45)
    industry = TextField(45)
    company_size = TextField(45)
    active = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.now)

    def __init__(self, name, email, password, company_name, industry, company_size):
        self.name = name
        self.email = email
        self.password = password
        self.company_name = company_name
        self.industry = industry
        self.company_size = company_size
        self.active = BooleanField(default=False)
        self.timestamp = datetime.now

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

