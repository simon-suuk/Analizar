from models.base_model import *
from peewee import CharField, BooleanField, TextField, DateTimeField

from datetime import datetime


class UserModel(BaseModel):
    name = TextField(45)
    email = TextField(45)
    password = TextField(45)
    company_name = TextField(45)
    industry = TextField(45)
    company_size = TextField(45)
    is_active = BooleanField(default=False)
    timestamp = DateTimeField(default=datetime.now)
