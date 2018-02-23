from models.base_model import *
from peewee import CharField, BooleanField, TextField, DateTimeField

from datetime import datetime


class UserModel(BaseModel):
    social_id = TextField(unique=True)
    username = TextField()
    email = TextField(null=True)
    password = TextField()
    is_active = BooleanField()
    timestamp = DateTimeField(default=datetime.now)
