from dotenv import load_dotenv
from mongoengine import connect
from models import Assets, Collection
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
        print(data)
        new_asset = Assets(
            asset_id = Assets.objects.count() + 1,
            creator = creator,
            policy_id = policy_id,
            token_name = token_name,
            royalti_address = royalti_address,
            royalti_percentag = royalti_percentag,
            asssetKey = asssetKey,
            price = price,
            collectionId = collectionId,
            like = [],
            data = json.loads(data)
        )
        new_asset.save()
        return ({'id': new_asset["asset_id"]})


def get_list(assets):
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
        data = get_list(assets)
        return data
    except Exception as e:
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get asset by id Data 
def get_assets_by_id(id):
    try:
        assets = Assets.objects.filter(asset_id=id)
        data = get_list(assets)
        return data
    except Exception as e:
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_all_assets_from_collection(policy_id):
    try:
        assets = Assets.objects.filter(policy_id=policy_id)
        data = get_list(assets)
        return data
    except Exception as e:
        return e

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_assets_by_collection_id(collection_id):
    try:
        assets = Assets.objects.filter(collectionId=collection_id)
        data = get_list(assets)
        return data
    except Exception as e:
        return e

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_collections():
    try:
        data = Assets.objects.order_by().values_list('policy_id').distinct('policy_id')
        return data
    except Exception as e:
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_assets_creator(creator):
    try:
        assets = Assets.objects.filter(creator=creator)
        print(assets)
        data = get_list(assets)
        return data
    except Exception as e:
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get Assets Between two dates  
def get_assets_between_dates(start_date,end_date):
    try:
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        assets = Assets.objects.filter(listing_date__gte=start_date,listing_date__lte=end_date)
        data = get_list(assets)
        return data
    except Exception as e:
        print(e)
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get All collection Data 
def get_all_collection():
    try:
        collections = Collection.objects.all()
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
    except Exception as e:
        return e    


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get All collection Data 
def get_users_collection(username):
    try:
        collections = Collection.objects.filter(username=username)
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
    except Exception as e:
        return e    


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_collection_by_id(collection_id):
    try:
        assets = Collection.objects.filter(collection_id=collection_id)
        asset = []
        for data in assets:
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
    except Exception as e:
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get collection Data 
def get_collection_by_category(category):
    try:
        assets = Collection.objects.filter(category=category)
        asset = []
        for data in assets:
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
    except Exception as e:
        return e


def insert_collection(username,name,image, url, desc,category):
    print(name,image, url, desc,category)
    new_asset = Collection(
        collection_id = Collection.objects.count() + 1,
        username=username,
        name = name,
        image = image,
        url = url,
        category = category,
        desc = desc
    )
    new_asset.save()
    return ({'id': new_asset["collection_id"]})

