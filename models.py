from typing import Dict
from unicodedata import decimal
import uuid
from xmlrpc.client import Boolean
from mongoengine.document import Document
from mongoengine.fields import EmailField, StringField, UUIDField, ListField, IntField, DateTimeField,DecimalField,BooleanField,DictField
import datetime

# inheriting from Document class
class User(Document):
    meta = {"collection": "User"}
    uuid=UUIDField()
    username=StringField(unique=True,required=True, max_length=100)
    name=StringField(required=True, max_length=100)
    picture=StringField(required=True)
    email=EmailField()
    bio = StringField(required=False,max_length=10000)
    wallete_address = StringField(required=False,max_length=500)
    srks_id=StringField(required=True,max_length=100)
    following_username = ListField()
    follower_username = ListField()
    liked_asset = ListField()
    access = StringField(required=True, max_length=100)
    password = StringField(max_length=100)


class Assets(Document):
    meta = {"collection": "Assets"}
    asset_id = IntField(min_value=1)
    creator = StringField(required=True, max_length=500)
    policy_id = StringField(required=True, max_length=500)
    token_name = StringField(required=True, max_length=500)
    royalti_address = StringField(required=True, max_length=500)
    royalti_percentag = IntField()
    asssetKey = StringField(required=True, max_length=500)
    price = DecimalField(required=True)
    collectionId = IntField()
    like = ListField()
    data = DictField()
    listing_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)
    collected_user = StringField(max_length=150)
    def save(self, *args, **kwargs):
        if not self.listing_date:
            self.listing_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Assets, self).save(*args, **kwargs)


class Transactions(Document):
    meta = {"collection": "Transactions"}
    asset_id = IntField(min_value=1)
    event = StringField(required=True, max_length=50)
    to = StringField(required=True, max_length=500)
    From = StringField(required=True, max_length=500)
    price = StringField(required=True, max_length=100)
    timestamp = DateTimeField(default=datetime.datetime.now)


class Collections(Document):
    meta = {"collection": "Collections"}
    collection_id = IntField(min_value=1)
    username=StringField(required=True, max_length=100)
    name = StringField(required=True, max_length=500)
    image = StringField(required=True, max_length=500)
    url = StringField(required=True, max_length=1500)
    category = StringField(required=True, max_length=500)
    desc = StringField(required=True, max_length=5000)
    isFeatured = BooleanField()
    listing_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)
    def save(self, *args, **kwargs):
        if not self.listing_date:
            self.listing_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        return super(Collections, self).save(*args, **kwargs)
