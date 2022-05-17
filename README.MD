# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

Marketplace User API documantation.

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

Run API project Locally.

clone the project.
Create a python virtual environment using virtualenv venv.
Run pip install -r requirements.txt  to install all the required dependencies.
Install MongoDB. 
Start the project using python run app.py

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


Endpoints (URL's are Rlated to Local System):-

(1) Work : Login
Method : GET
URL : http://127.0.0.1:5000/api/login 
response :- {FRONTEND_URL}(defiened in the .env file)?jwt={Token}
example :- http://localhost:3000/?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjY5ODQwMywianRpIjoiMTkyM2ZmMGMtN2MwNi00NDY4LTk3YWEtNTg3OTdlZGUzNTJkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlRYZ0tTOXV5b24xMjNSZUJQdjRIOHpUIiwibmJmIjoxNjUyNjk4NDAzLCJleHAiOjE2NTI2OTkzMDN9.n3y1paZrkUZh1wHUXdKXZ0zHQw_6D5xbf7goBqOwbcY


# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------


(2)Work : Logout and clear cookies
Method : POST
URL : http://127.0.0.1:5000/api/logout 
response :- {
    "msg": "logout successful"
}

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

(3) Work: Profile
Method: GET
URL: http://127.0.0.1:5000/api/Profile 
with the header: Authorization Bearer Token
response:- 
If the token is valid: User's data in JSON format
If the token is not valid: {
    "msg": "Token has expired"
}

example :- http://127.0.0.1:5000/api/Profile 
header : Authorization Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjY5NTgzNywianRpIjoiMDAxMzAxZDMtZTllNi00NTE3LWJkMmQtNThhODg2ZDI1ZTQyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlRYZ0tTOXV5b24xMjNSZUJQdjRIOHpUIiwibmJmIjoxNjUyNjk1ODM3LCJleHAiOjE2NTI2OTY3Mzd9.SEY_yNqjL1iGgIi_Dff261738llmp23pSSs2pZFOmag

response :- {
    "data": {
        "email": "akashpalan@lampros.tech",
        "name": "Akash",
        "picture": "public/upload/common/user_404.jpg",
        "username": "Akash114"
    },
    "status": 200,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjcwMTE1NywianRpIjoiNjZiMDlkYTEtOWU2My00NTk5LThlMzUtMjY3ZTg1N2ZjMWVhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IlRYZ0tTOXV5b24xMjNSZUJQdjRIOHpUIiwibmJmIjoxNjUyNzAxMTU3LCJleHAiOjE2NTI3MDIwNTd9.8cJ4g_Q6JM78lhBeq02O4wG6azZtg_TmN09xZE7znLw"
}

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

(4) Work: All the User's Data
Method: GET
URL: http://127.0.0.1:5000/api/getUsers 
response:- 
If the token is valid: All User's data in JSON format

Example:
response :
{
    "data": [
        {
            "email": "akashpalan@lampros.tech",
            "name": "Akash",
            "picture": "public/upload/common/user_404.jpg",
            "username": "Akash114"
        }
    ],
    "status": 200
}

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
