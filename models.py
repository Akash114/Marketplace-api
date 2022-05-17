
from mongoengine.document import Document
from mongoengine.fields import EmailField, StringField, UUIDField

# inheriting from Document class
class User(Document):
    meta = {"collection": "User"}
    uuid=UUIDField()
    username=StringField(required=True, max_length=100)
    name=StringField(required=True, max_length=100)
    picture=StringField(required=True)
    email=EmailField()
    srks_id=StringField(required=True,max_length=100)

  
