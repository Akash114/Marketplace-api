from unicodedata import name
from dotenv import load_dotenv
from mongoengine import connect
from models import User
import uuid
import os


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Connecting to MongoDb cluster 
def connect_db():
    try:
        load_dotenv()
        connect(host=os.getenv("CLUSTER_URL"))
        print("Database cluster connected")
    except Exception as e:
        print(e.args)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Inter Users Data To DB 
def insert_into_db(username,name, email, picture,id):
    try:
        try:
            user = User.objects.get(username=username)
            print({"_id": str(user["id"]), "message": "User already exists"})
        except:
            new_user = User(
                username=username, 
                uuid=uuid.uuid4().hex,
                name=name,
                email=email,
                picture=picture,
                srks_id=id
            )
            new_user.save()
            print({"_id": str(new_user["id"]), "message": "User created"})
    except Exception as e:
        print({"error": e.args})


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get Single User's Data based On srks_id 
def get_user(srks_id):
    try:
        user = User.objects.get(srks_id=srks_id)
        return user
    except:
        return False


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get All users Data 
def get_all_users():
    return User.objects.all()