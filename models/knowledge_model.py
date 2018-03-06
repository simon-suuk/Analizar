from peewee import TextField, ForeignKeyField

from models.base_model import *


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
