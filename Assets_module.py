from dotenv import load_dotenv
from mongoengine import connect
from models import Assets
import uuid
import os
from datetime import datetime

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
def insert_asset(creator,policy_id, token_name, royalti_address,royalti_percentag,asssetKey,price,collectionId):
    try:
        assets = Assets.objects.filter(policy_id = policy_id).filter(token_name= token_name)
        print(assets)
        if not assets:
            print(1/0)
        return ("Asset already exists")
    except Exception as e:
        print(e)
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
            like = []
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


