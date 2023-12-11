from flask import request
import uuid
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from schema import StoreSchema
from db import db

from models.store import StoreModel

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from flask_jwt_extended import jwt_required


#Creating a BluePrint for a particular API endpoint group here it is Store

blp = Blueprint("Stores",__name__, description = "Operations on Stores")

# Creating the Method View --- These are classes where each method maps to one endpoint



@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    @jwt_required()
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        
        return {"message":"Store Successfully Deleted"},200


@blp.route("/store")
class Store(MethodView):
    @jwt_required()
    @blp.response(200,StoreSchema(many=True))
    def get(self):
      # return stores.values()
      # print(stores.values())
      # return stores

      return StoreModel.query.all()
    
    @jwt_required()
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,storeData):
        # storeData = request.get_json()
        
        # Checking if the name key is not in the storeData

        # if("name" not in storeData):
        #     abort(400, message="Bad request. Ensure 'name' is included in the JSON payload")
        

        # Checking if the Store is already present in that store or not

        # for store in stores.values():
        #     if(storeData["name"] == store["name"]):
        #         abort(400,message="Store already exist")

        # store_id = uuid.uuid4().hex
        
        # new_store = {
        #     **storeData, # This will make the value inside the storeData in a key value pair
        #     "id":store_id
        # }
        
        # stores[store_id] = new_store
        # return new_store


        ### After Database Integration ###
        
        store = StoreModel(**storeData)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store


