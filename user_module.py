from unicodedata import name
from dotenv import load_dotenv
from mongoengine import connect
from models import User
import uuid
import os

DB_NAME="users"
CLUSTER_URL="mongodb+srv://DM:dm123@dm.bdlnk.mongodb.net/?retryWrites=true&w=majority"

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Connecting to MongoDb cluster 
def connect_db():
    try:
        load_dotenv()
        connect(alias="default",host=CLUSTER_URL)
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
            user = User.objects.get(srks_id=id)
            print({"_id": str(user["id"]), "message": "User already exists"})
        except:
            new_user = User(
                username=username, 
                uuid=uuid.uuid4().hex,
                name=name,
                email=email,
                picture=picture,
                srks_id=id,
                following_username=[],
                follower_username=[],
                access= 'Grant'
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
        data = User.objects.filter(srks_id=srks_id)
        users = []
        for user in data:
            users.append({
            "status":200,
            "data":
            {
                "name": user.name,
                "username":user.username,
                "picture":user.picture,
                "email":user.email,
                "bio":user.bio,
                "following_username":user.following_username,
                "follower_username":user.follower_username,
                "liked_asset":user.liked_asset,
                "access":user.access
            }
            })
        return users
    except:
        return False


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get All users Data 
def get_all_users():
    return User.objects.all()


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#add follower 
def request_add_follower(follower_username,following_username):
    try:
        follower_user = User.objects.get(username=follower_username)
        following_user = User.objects.get(username=following_username)
        follower_user.following_username.append(following_username)
        following_user.follower_username.append(follower_username)
        follower_user.save()
        following_user.save()
        return "Follower Added Sucessfully !"
    except Exception as e:
        print(e)    
        return "User Does Not Exists !"



# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#get follower 
def request_get_follower(username):
    try:
        user = User.objects.get(username=username)
        return user.follower_username
    except Exception as e:
        print(e)    
        return "User Does Not Exists !"
    

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#get acesss 
def request_get_access(username):
    try:
        user = User.objects.get(username=username)
        return user.access
    except Exception as e:
        print(e)    
        return "User Does Not Exists !"


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#set acesss 
def request_set_access(username,access_type):
    try:
        user = User.objects.get(username=username)
        user.access = access_type
        user.save()
        return "Access set to " + user.access
    except Exception as e:
        print(e)    
        return "User Does Not Exists !"

