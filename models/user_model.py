from models.base_model import *
from peewee import BooleanField, TextField, DateTimeField
from flask_login import UserMixin
from datetime import datetime


class UserModel(BaseModel):
    name = TextField(45)
    email = TextField(45)
    password_hash = TextField(255)
    company_name = TextField(45)
    industry = TextField(45)
    company_size = TextField(45)
    active = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.now)
    social_id = TextField(unique=True, null=True)
    social_username = TextField(null=True)
    social_email = TextField(null=True)
    page_id = TextField(null=True)
    access_token = TextField(null=True)
