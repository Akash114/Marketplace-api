from dotenv import load_dotenv
from mongoengine import connect
from models import Transactions, Collection
import uuid
import os
from datetime import datetime
DB_NAME="users"
CLUSTER_URL="mongodb+srv://DM:dm123@dm.bdlnk.mongodb.net/?retryWrites=true&w=majority"

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
def insert_transaction(asset_id,event, to, From,price):
    new_asset = Transactions(
        asset_id = asset_id,
        event = event,
        to = to,
        From = From,
        price = price
    )
    new_asset.save()
    return ({'id': new_asset["asset_id"]})


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


def get_list(tansactions):
    asset = []
    for data in tansactions:
        asset.append(
            {
        "asset_id": data.asset_id,
        "event":data.event,
        "to":data.to,
        "From":data.From,
        'price':data.price,
        "timestamp": data.timestamp
        }
        )
    return asset

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
#Get All assets Data 
def get_all_transactions():
    try:
        transaction = Transactions.objects.all()
        data = get_list(transaction)
        return data
    except Exception as e:
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get Asset transaction Data 
def get_asset_transactions(id):
    try:
        transaction = Transactions.objects.filter(asset_id=id)
        data = get_list(transaction)
        return data
    except Exception as e:
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get event transaction Data 
def get_event_transactions(event):
    try:
        transaction = Transactions.objects.filter(event=event)
        data = get_list(transaction)
        return data
    except Exception as e:
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get transaction of address 
def get_address_transactions(address):
    try:
        transaction = Transactions.objects.filter(to=address) or Transactions.objects.filter(From=address)
        data = get_list(transaction)
        return data
    except Exception as e:
        print(e)
        return e


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get transactions Between two dates  
def get_transactions_between_dates(start_date,end_date):
    try:
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        assets = Transactions.objects.filter(timestamp__gte=start_date,timestamp__lte=end_date)
        data = get_list(assets)
        return data
    except Exception as e:
        print(e)
        return e
