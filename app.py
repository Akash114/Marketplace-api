#important libraries
from urllib import response
from flask import Flask
import json
from flask import Flask,redirect, jsonify
from flask.wrappers import Response
from flask.globals import request, session
import requests
from user_module import *
import jwt
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
import base64   
from datetime import datetime, timedelta, timezone
from Assets_module import *
from transaction_module import *

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#App configurations
app = Flask(__name__)

cors = CORS(app)
load_dotenv()
app.config['Access-Control-Allow-Origin'] = '*'
app.config["Access-Control-Allow-Headers"]="Content-Type"
app.config['DEBUG'] = os.getenv('DEBUG')


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

AUTH="trxquUHCitAZOTlVWAre"
ID="6194228"
BACKEND_URL="https://api.demo-server.tk/"
FRONTEND_URL="https://nft.demo-server.tk/"
ALGORITHM="HS256"
DEBUG=True
app.config["JWT_SECRET_KEY"]="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

connect_db()


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#App Home Page

@app.route('/api/')
def home():
    return {"Hello": "World"}, 200


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Login API
@app.route('/api/login', methods=["GET"])
def getToken(): 
    auth = base64.b64encode(AUTH.encode('ascii')).decode("utf-8") 
    id = base64.b64encode(ID.encode('ascii')).decode("utf-8") 
    response = jsonify({'redirect_url': 'http://decentralizemusic.com/v1/oauth/login?auth='+str(auth)+'&client_id='+str(id)})
    return response


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#To refresh expiring Token 
@app.after_request
def refresh_expiring_jwts(response):
    try:
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        # Case where there is not a valid JWT. Just return the original respone
        return response


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Callback Function to get User Data
@app.route('/getCallback', methods=["GET"])
def getCallback(): 
    try:
        state = request.args.get('state')
        srks_id = base64.b64decode(state.encode('ascii')).decode("utf-8")
        if get_user(srks_id):
            jwt_token=create_access_token(srks_id)
            return redirect(f"{FRONTEND_URL}?jwt={jwt_token}") 
        else:
            response = requests.post(
                'http://decentralizemusic.com/api/v1/user_oauth',params={'state':state}
            )
            user_data = response.json()['data']
            print(user_data)

            username = user_data['username']
            name = user_data['first_name'] + user_data['last_name']
            email = user_data['email']
            picture = user_data['photo']
            id = srks_id
            insert_into_db(username,name, email, picture,id)
            jwt_token=create_access_token(srks_id)
            return redirect(f"{FRONTEND_URL}?jwt={jwt_token}") 
    except Exception as e:
        return jsonify({'error':str(e)})


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#API Logout Function

@app.route("/api/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get Single User Profie based on Access Token
@app.route('/api/profile')
@jwt_required()
def my_profile():
    user = get_user(get_jwt_identity())
    response_body = {
        "status":200,
        "data":
        {
        "name": user.name,
        "username":user.username,
        "picture":user.picture,
        "email":user.email
        }
    }

    return response_body


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
#Get All User Profie 
@app.route('/api/getUsers')
def get_users():
    users = get_all_users()
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
    response_body = {
        "status":200,
        "data":all_users
    }
    return response_body


@app.route('/api/addFollower',methods=["POST"])
@jwt_required()
def add_follower():
    try:
        user = get_user(get_jwt_identity())
        following_username = request.args.get('following_username')
        request_add_follower(user.username,following_username)
        response_body = {
        "status":200,
        "data":'Follower Added Sucessfully'
        }
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getFollower',methods=["GET"])
def get_follower():
    try:
        username = request.args.get('username')
        followers = request_get_follower(username)
        response_body = {
        "status":200,
        "data":followers
        }
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getAccess',methods=["GET"])
def get_access():
    try:
        username = request.args.get('username')
        access = request_get_access(username)
        response_body = {
        "status":200,
        "data":access
        }
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/setAccess',methods=["GET"])
def set_access():
    try:
        username = request.args.get('username')
        access_type = request.args.get('access_type')
        access = request_set_access(username,access_type)
        response_body = {
        "status":200,
        "data":access
        }
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


#---------------------------------- Asset APIs ----------------------------#
@app.route('/api/listAsset',methods=["POST"])
def listAsset():
    try:
        creator = request.json.get('creator')
        policy_id = request.json.get('policy_id')
        token_name = request.json.get('token_name')
        royalti_address = request.json.get('royalti_address')
        royalti_percentag = request.json.get('royalti_percentag')
        asssetKey = request.json.get('asssetKey')
        price = request.json.get('price')
        collectionId = request.json.get('collectionId')
        data_= request.json.get('data')
        data = insert_asset(creator,policy_id, token_name, royalti_address,royalti_percentag,asssetKey,price,collectionId,data_)
        response_body = {
        "status":200,
        "data": str(data)
        }
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getAllAssets',methods=["GET"])
def getAllAssets():
    try:
        data = get_all_assets()
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getAsset',methods=["GET"])
def getAsset():
    try:
        id = request.args.get('asset_id')
        data = get_assets_by_id(id)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})



@app.route('/api/getAssetByPolicy',methods=["GET"])
def getAssetByPolicy():
    try:
        id = request.args.get('policy_id')
        data = get_all_assets_from_collection(id)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getAssetByCollection',methods=["GET"])
def getAssetByCollection():
    try:
        id = request.args.get('collection_id')
        data = get_assets_by_collection_id(id)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})



@app.route('/api/getCollectionById',methods=["GET"])
def getCollectionById():
    try:
        id = request.args.get('collection_id')
        data = get_collection_by_id(id)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getCollectionByCategory',methods=["GET"])
def getCollectionByCategory():
    try:
        id = request.args.get('category')
        data = get_collection_by_category(id)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})




@app.route('/api/getCollections',methods=["GET"])
def getCollections():
    try:
        data = get_collections()
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getCollectionByUser',methods=["GET"])
def getCollectionByUser():
    try:
        username = request.args.get('username')
        data = get_users_collection(username)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body

    except Exception as e:
        print(e)



@app.route('/api/getAssetByCrator',methods=["GET"])
def getAssetByCreator():
    try:
        id = request.args.get('creator_address')

        data = get_assets_creator(id)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getAssetByDate',methods=["GET"])
def getAssetByDate():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        data = get_assets_between_dates(start_date,end_date)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


#---------------------------------- Transactions APIs ----------------------------#
@app.route('/api/addTransaction',methods=["POST"])
def addTransaction():
    try:
        asset_id = request.args.get('asset_id')
        event = request.args.get('event')
        to = request.args.get('to')
        From = request.args.get('From')
        price = request.args.get('price')
        data = insert_transaction(asset_id,event, to, From, price)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/addCollection',methods=["POST"])
@jwt_required()
def addCollection():
    try:
        user = get_user(get_jwt_identity())
        name = request.args.get('name')
        image = request.args.get('image')
        url = request.args.get('url')
        category = request.args.get('category')
        desc = request.args.get('desc')
        print(user)
        data = insert_collection(user.username,name,image, url, desc,category)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        print(e)
        return jsonify({'error':str(e)})


@app.route('/api/getAllCollections',methods=["GET"])
def getAllCollections():
    try:
        data = get_all_collection()
        response_body = {
                "status":200,
                "data": data
                }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getAssetTransactions',methods=["GET"])
def getAssetTransactions():
    try:
        asset_id = request.args.get('asset_id')
        data = get_asset_transactions(asset_id)
        response_body = {
                "status":200,
                "data": data
                }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getEventTransactions',methods=["GET"])
def getEventTransactions():
    try:
        event = request.args.get('event')
        data = get_event_transactions(event)
        response_body = {
                "status":200,
                "data": data
                }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getAddressTransactions',methods=["GET"])
def getAddressTransactions():
    try:
        address = request.args.get('address')
        data = get_address_transactions(address)
        response_body = {
                "status":200,
                "data": data
                }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getTransactionByDate',methods=["GET"])
def getTransactionByDate():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        data = get_transactions_between_dates(start_date,end_date)
        response_body = {
            "status":200,
            "data": data
            }       
        return response_body
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/api/search',methods=["POST"])
def getSearchResult():
    try:
        query = request.json.get('query')
        data = search(query)
        response_body = {
            "status":200,
            "data": data
            } 
        return response_body 
    except Exception as e:
        return jsonify({'error':str(e)})



@app.route('/api/makeFeaturedCollection')
def addFeaturedCollection():
    try:
        collection_id = request.json.get('collection_id')
        data = add_featured_collection(collection_id)
        response_body = {
            "status":200,
            "data": data
            } 
        return response_body 
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/removeFeaturedCollection')
def removeFeaturedCollection():
    try:
        collection_id = request.json.get('collection_id')
        data = remove_featured_collection(collection_id)
        response_body = {
            "status":200,
            "data": data
            } 
        return response_body 
    except Exception as e:
        return jsonify({'error':str(e)})


@app.route('/api/getHotCollection')
def featuredCollection():
    try:
        data = get_featured_collection()
        response_body = {
            "status":200,
            "data": data
            } 
        return response_body 
    except Exception as e:
        return jsonify({'error':str(e)})



if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
