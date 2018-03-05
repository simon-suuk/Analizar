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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GeneralKnowledgeBase(BaseModel):
    general_advice = TextField(null=True, unique=True)


class ReachKnowledgeBase(BaseModel):
    location = TextField(null=True)
    other_business_page_and_location = TextField(null=True)
    influencers = TextField(null=True)
    trends_and_events = TextField(null=True)
    audience_active_time = TextField(null=True, unique=True)
    circle_of_friends = TextField(null=True)
    tag_people = TextField(null=True)
    post_frequency = TextField(null=True)
    post_boost = TextField(null=True)


class EngagementKnowledgeBase(BaseModel):
    general_advice = ForeignKeyField(GeneralKnowledgeBase, to_field="general_advice",
                                     related_name="knowledge from general_advice")
    audience_active_time = ForeignKeyField(ReachKnowledgeBase, to_field="audience_active_time",
                                           related_name="knowledge from ReachKnowledgeBase")
    audience_demography = TextField(null=True)


class NegativeFeedbackKnowledgeBase(BaseModel):
    general_advice = ForeignKeyField(GeneralKnowledgeBase, to_field="general_advice",
                                     related_name="knowledge from general_advice")


class PageFollowKnowledgeBase(BaseModel):
    general_advice = ForeignKeyField(GeneralKnowledgeBase, to_field="general_advice",
                                     related_name="knowledge from general_advice")
    other_business_page = TextField(null=True)
