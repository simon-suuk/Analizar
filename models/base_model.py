import os
from peewee import Model
from flask_login import UserMixin
from playhouse.pool import PooledPostgresqlDatabase

db_name = os.environ.get("DB_NAME")
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")


class DBSingleton():
    db = None

    @classmethod
    def getInstance(cls):
        if not cls.db:
            cls.db = PooledPostgresqlDatabase(db_name, **{'user': db_user,
                                                          'host': db_host,
                                                          'password': db_password})

        return cls.db


class BaseModel(UserMixin, Model):
    class Meta:
        database = DBSingleton.getInstance()
