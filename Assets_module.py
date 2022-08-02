import re
from dotenv import load_dotenv
from mongoengine import connect
from models import Assets, Collections, User
import uuid
import os
from datetime import datetime
import json
# DB_NAME="users"
# CLUSTER_URL="mongodb+srv://DM:dm123@dm.bdlnk.mongodb.net/?retryWrites=true&w=majority"

# # ---------------------------------------------------------------------------------------
# # ---------------------------------------------------------------------------------------
# # ---------------------------------------------------------------------------------------
# #Connecting to MongoDb cluster 
# def connect_db():
#     try:
#         load_dotenv()
#         connect(host=CLUSTER_URL)
#         print("Database cluster connected")
#     except Exception as e:
#         print(e.args)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Inter Assets Data To DB 
def insert_asset(creator,policy_id, token_name, royalti_address,royalti_percentag,asssetKey,price,collectionId,data):
    try:
        assets = Assets.objects.filter(policy_id = policy_id).filter(token_name= token_name)
        print(assets)
        if not assets:
            print(1/0)
        return ("Asset already exists")
    except Exception as e:
        new_asset = Assets(
            asset_id = Assets.objects.count() + 1,
            creator = creator,
            policy_id = policy_id,
            token_name = token_name,
            royalti_address = royalti_address,
            royalti_percentag = royalti_percentag,
            asssetKey = str(asssetKey),
            price = price,
            collectionId = collectionId,
            like = [],
            data = data
        )
        new_asset.save()
        return ({'id': new_asset["asset_id"]})


def get_list_asset(assets):
    asset = []
    for data in assets:
        asset.append(
            {
        "asset_id": data.asset_id,
        "creator":data.creator,
        "policy_id":data.policy_id,
        "token_name":data.token_name,
        "royalti_address": data.royalti_address,
        "royalti_percentag":data.royalti_percentag,
        "like":data.like,
        "listing_date":data.listing_date,
        "modified_date":data.modified_date,
        "asssetKey":data.asssetKey,
        "price":data.price,
        "collectionId":data.collectionId,
        "data":data.data
        }
        )
    return asset

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get All assets Data 
def get_all_assets():
    try:
        assets = Assets.objects.all()
        data = get_list_asset(assets)
        return data
    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get asset by id Data 
def get_assets_by_id(id):
    try:
        assets = Assets.objects.filter(asset_id=id)
        data = get_list_asset(assets)
        return data
    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_all_assets_from_collection(policy_id):
    try:
        assets = Assets.objects.filter(policy_id=policy_id)
        data = get_list_asset(assets)
        return data
    except Exception as e:
        return str(e)

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_assets_by_collection_id(collection_id):
    try:
        assets = Assets.objects.filter(collectionId=collection_id)
        data = get_list_asset(assets)
        return data
    except Exception as e:
        return str(e)

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_collections():
    try:
        data = Assets.objects.order_by().values_list('policy_id').distinct('policy_id')
        return data
    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_assets_creator(creator):
    try:
        assets = Assets.objects.filter(creator=creator)
        print(assets)
        data = get_list_asset(assets)
        return data
    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get Assets Between two dates  
def get_assets_between_dates(start_date,end_date):
    try:
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        assets = Assets.objects.filter(listing_date__gte=start_date,listing_date__lte=end_date)
        data = get_list_asset(assets)
        return data
    except Exception as e:
        print(e)
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get All collection Data 
def get_all_collection():
    try:
        collections = Collections.objects.all()
        data = get_list_collection(collections)
        return data
    except Exception as e:
        return str(e)    


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get All collection Data 
def get_users_collection(username):
    try:
        collections = Collections.objects.filter(username=username)
        data = get_list_collection(collections)
        return data
    except Exception as e:
        return str(e)    


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_collection_by_id(collection_id):
    try:
        assets = Collections.objects.filter(collection_id=collection_id)
        data = get_list_collection(assets)
        return data

    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_collection_by_category(category):
    try:
        assets = Collections.objects.filter(category=category)
        data = get_list_collection(assets)
        return data
    except Exception as e:
        return str(e)


def insert_collection(username,name,image, url, desc,category):
    try:
        new_collection = Collections()
        new_collection.collection_id = Collections.objects.count() + 1
        new_collection.username=username
        new_collection.name = name
        new_collection.image = image
        new_collection.url = url
        new_collection.category = category
        new_collection.desc = desc
        new_collection.isFeatured = False        
        new_collection.save()
        return ({'id': new_collection["collection_id"]})
    except Exception as e:
        print('-----',e)
        return str(e)


def get_list_collection(collections):
    asset = []
    for data in collections:
        asset.append(
            {
        "collection_id": data.collection_id,
        "username":data.username,
        "name":data.name,
        "image":data.image,
        'url':data.url,
        "category": data.category,
        "desc":data.desc
        }
        )
    return asset

def get_list_user(users):
    all_users = []
    for user in users:
        all_users.append(
            {
        "name": user.name,
        "username":user.username,
        "picture":user.picture,
        "email":user.email
        }
        )
    return all_users


def search(query):
    try:
        collections = Collections.objects.filter(name= re.compile('.*'+ query +'.*', re.IGNORECASE)) or Collections.objects.filter(category=re.compile('.*'+ query +'.*', re.IGNORECASE)) or Collections.objects.filter(desc=re.compile('.*'+ query +'.*', re.IGNORECASE))
        users = User.objects.filter(name= re.compile('.*'+ query +'.*', re.IGNORECASE)) or User.objects.filter(username=re.compile('.*'+ query +'.*', re.IGNORECASE)) or User.objects.filter(email=re.compile('.*'+ query +'.*', re.IGNORECASE))
        asset = Assets.objects.filter(token_name= re.compile('.*'+ query +'.*', re.IGNORECASE)) or Assets.objects.filter(listing_date=re.compile('.*'+ query +'.*', re.IGNORECASE)) or Assets.objects.filter(policy_id=re.compile('.*'+ query +'.*', re.IGNORECASE)) or Assets.objects.filter(creator=re.compile('.*'+ query +'.*', re.IGNORECASE))
        data = {
          'collection_data':get_list_collection(collections),
          'user_data':get_list_user(users),
          'asset_data':get_list_asset(asset)
        }
        return data
    except Exception as e:
        return str(e)    


def add_featured_collection(id):
    try:
        collections = Collections.objects.get(collection_id= id)
        collections.update(isFeatured=True)
        # collections.save()
        return str(collections.name) + " is Added To Featured Collection"
    except Exception as e:
        print(e)
        return str(e)


def remove_featured_collection(id):
    try:
        collections = Collections.objects.get(collection_id= id)
        collections.update(isFeatured=False)
        return str(collections.name) + " is Removed To Featured Collection"
    except Exception as e:
        print(e)
        return str(e)        


def get_featured_collection():
    try:
        collections = Collections.objects.filter(isFeatured= True)
        data = get_list_collection(collections)
        return data
    except Exception as e:
        return str(e)        