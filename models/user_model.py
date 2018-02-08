from models.base_model import *
from peewee import CharField, BooleanField, TextField, DateTimeField

from datetime import datetime


class UserModel(BaseModel):
    username = TextField(45)
    usersecret = TextField(45)
    is_active = BooleanField()
    timestamp = DateTimeField(default=datetime.now)
