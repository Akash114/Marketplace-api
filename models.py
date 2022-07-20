from mongoengine.document import Document
from mongoengine.fields import EmailField, StringField, UUIDField, ListField

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
    access = StringField(required=True, max_length=100)

class NFT(Document):
    policy_id = StringField(required=True, max_length=100)
    token_name = StringField(required=True, max_length=100)
    like = ListField()

