from unicodedata import decimal
import uuid
from mongoengine.document import Document
from mongoengine.fields import EmailField, StringField, UUIDField, ListField, IntField, DateTimeField,DecimalField
import datetime

# inheriting from Document class
class User(Document):
    meta = {"collection": "User"}
    uuid=UUIDField()
    username=StringField(required=True, max_length=100)
    name=StringField(required=True, max_length=100)
    picture=StringField(required=True)
    email=EmailField()
    srks_id=StringField(required=True,max_length=100)
    following_username = ListField()
    follower_username = ListField()
    liked_asset = ListField()
    access = StringField(required=True, max_length=100)


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
    collectionId = StringField(required=True, max_length=500)
    like = ListField()
    listing_date = DateTimeField()
    modified_date = DateTimeField(default=datetime.datetime.now)

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


class Collection(Document):
    meta = {"collection": "Collections"}
    collection_id = IntField(min_value=1)
    username=StringField(required=True, max_length=100)
    name = StringField(required=True, max_length=500)
    image = StringField(required=True, max_length=500)
    url = StringField(required=True, max_length=1500)
    category = StringField(required=True, max_length=500)
    desc = StringField(required=True, max_length=5000)