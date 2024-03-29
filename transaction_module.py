from dotenv import load_dotenv
from mongoengine import connect
from models import Transactions
import uuid
import os
from datetime import datetime
import pandas as pd 

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


def get_list_tansaction(tansactions):
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
#Get All assets Data 
def get_all_transactions():
    try:
        transaction = Transactions.objects.all()
        data = get_list_tansaction(transaction)
        return data
    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get Asset transaction Data 
def get_asset_transactions(id):
    try:
        transaction = Transactions.objects.filter(asset_id=id)
        data = get_list_tansaction(transaction)
        return data
    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get event transaction Data 
def get_event_transactions(event):
    try:
        transaction = Transactions.objects.filter(event=event)
        data = get_list_tansaction(transaction)
        return data
    except Exception as e:
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get transaction of address 
def get_address_transactions(address):
    try:
        transaction = Transactions.objects.filter(to=address) or Transactions.objects.filter(From=address)
        data = get_list_tansaction(transaction)
        return data
    except Exception as e:
        print(e)
        return str(e)


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get transactions Between two dates  
def get_transactions_between_dates(start_date,end_date):
    try:
        start_date = datetime.strptime(start_date, '%d/%m/%Y')
        end_date = datetime.strptime(end_date, '%d/%m/%Y')
        assets = Transactions.objects.filter(timestamp__gte=start_date,timestamp__lte=end_date)
        data = get_list_tansaction(assets)
        return data
    except Exception as e:
        print(e)
        return str(e)


def get_transactions_count_dates():
    try:
        transaction = Transactions.objects.all()
        data = get_list_tansaction(transaction)
        df = pd.DataFrame(data)
        filtered_data = df.groupby([df['timestamp'].dt.date]).count()['timestamp']
        filtered_data.index = filtered_data.index.map(str)

        final_data = {
            'dates':list(filtered_data.to_dict().keys()),
            'count':list(filtered_data.to_dict().values())
        }
        return final_data
    except Exception as e:
        return str(e)
