from flask import Flask,request,jsonify
from db import db

from flask_smorest import abort, Api
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

from flask_migrate import Migrate

from models.item import ItemModel
from models.store import StoreModel

from flask_jwt_extended import JWTManager

from blocklist import BLOCKLIST

# configuration of the flask

app = Flask(__name__)

# Configuration for the Blueprint

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"


app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


# Configuration for the SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///stores.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connecting the database with the flask app

db.init_app(app)

# Using the flask app with the Migrate and connecting with the database

migrate = Migrate(app,db)


# This connect the Flask-smorest with the Flask App

api = Api(app)

# Setting up the secret key for the JWT Token
app.config["JWT_SECRET_KEY"] = "Sneh Joshi"

## str(secrets.SystemRandom().getrandbits(128)) Use this as a secret key

jwt = JWTManager(app)

# Since we are using the flask_migrate then we donot want the sqlalchemy to create it

# with app.app_context():
#      db.create_all()

## Checking if the function is in the blacklist set or not

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    print(jwt_header)
    print(jwt_payload)
    return jwt_payload["jti"] in BLOCKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )

## If the JWT token has been expired then for that we have to use this function 

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )


# Registering the Blueprint

api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
api.register_blueprint(TagBlueprint)
api.register_blueprint(UserBlueprint)


# @app.get("/store")
# def get_all_stores():
#     # return {"stores":list(stores.values())}
#     return stores


# @app.post("/store")
# def create_store():
#     storeData = request.get_json()
#     print(storeData)
    
#     # Checking if the name key is not in the storeData

#     if("name" not in storeData):
#         abort(400, message="Bad request. Ensure 'name' is included in the JSON payload")
    

#     # Checking if the Store is already present in that store or not

#     for store in stores.values():
#         if(storeData["name"] == store["name"]):
#             abort(400,message="Store already exist")

#     store_id = uuid.uuid4().hex

#     new_store = {
#         **storeData, # This will make the value inside the storeData in a key value pair
#         "id":store_id
#     }

#     stores[store_id] = new_store
#     return new_store, 201


# @app.get("/item")
# def get_all_item():
#     # return {"item":list(items.values())}
#     return items


# # Add an Item in a Store of the Desired Match

# @app.post("/item")
# def create_item():
#     itemData = request.get_json()
    

#     if("price" not in itemData or "store_id" not in itemData or "name" not in itemData):
#         abort(400,message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload")

#     # Checking if the Item is already present in that store or not

#     for item in items.values():
#         if(itemData["name"] == item["name"] and itemData["store_id"] == item["store_id"]):
#             abort(400,message="Item already exist")

    
#     # Checking if the Store is present or not before adding the items 

#     if itemData["store_id"] not in stores:
#        abort(404,message="Store not Found") 
    
#     item_id = uuid.uuid4().hex

#     new_item = {
#         **itemData, # This will make the value inside the storeData in a key value pair
#         "id":item_id
#     }

#     items[item_id] = new_item
#     return new_item, 201
    



# # Get the Desired Store
# @app.get("/store/<string:store_id>")
# def get_store(store_id):
    
#     try:
#        return stores[store_id]
#     except:
#       abort(404,message="Store not Found")



# # Get the Desired Item
# @app.get("/item/<string:item_id>")
# def get_item(item_id):
    
#     try:
#        return items[item_id]
#     except:
#        abort(404,message="Item not Found")    



# # Delete the Desired Item
# @app.delete("/item/<string:item_id>")
# def delete_item(item_id):
    
#     try:
#        del items[item_id]
#        return {"message":"Item Deleted"}
#     except:
#        abort(404,message="Item not Found/Deleted")  



# # Delete the Desired Store
# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
    
#     try:
#        del stores[store_id]
#        return {"message":"Store Deleted"}
#     except:
#        abort(404,message="Store not Found/Deleted")  



# # Update the Desired Item
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
    
#     updatedItem = request.get_json() 

#     if "price" not in updatedItem or "name" not in updatedItem:
#         abort(400,message="Bad request. Ensure 'price' and 'name' are included in the JSON payload")
    
#     try:
#        currentItem =  items[item_id]
#        currentItem["name"] = updatedItem["name"]
#        currentItem["price"] = updatedItem["price"]
       
#        print(currentItem)
#        return {"message":"Item Updated"}
#     except:
#        abort(404,message="Item not Found/Deleted") 


if __name__ == "__main__":
    app.run(debug=True)


