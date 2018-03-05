from models.base_model import *
from peewee import CharField, BooleanField, TextField, DateTimeField, ForeignKeyField
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime


class UserModel(UserMixin, BaseModel):
    name = TextField(45)
    email = TextField(45)
    password_hash = TextField(255)
    company_name = TextField(45)
    industry = TextField(45)
    company_size = TextField(45)
    active = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.now)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

