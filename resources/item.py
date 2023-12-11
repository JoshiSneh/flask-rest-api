from flask import request
 
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from flask_jwt_extended import jwt_required

from schema import ItemSchema, ItemUpdateSchema

from models.item import ItemModel

from db import db


#Creating a BluePrint for a particular API endpoint group here it is Items


blp = Blueprint("Items",__name__, description = "Operations on Items")


# Creating the Method View --- These are classes where each method maps to one endpoint


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required() ### This is required for the JWT authorization
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
  
    @jwt_required() ### This is required for the JWT authorization
    def delete(self,item_id):
        #  return {"message":"Item Successfully Deleted"} 
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message":"Item Successfully Deleted"}
    
    @jwt_required() ### This is required for the JWT authorization
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemUpdateSchema)
    def put(self,updatedItem,item_id):
    
        # updatedItem = request.get_json() 

        # if "price" not in updatedItem or "name" not in updatedItem:
        #     abort(400,message="Bad request. Ensure 'price' and 'name' are included in the JSON payload")
        
        # try:
        #     currentItem =  items[item_id]
        #     currentItem["name"] = updatedItem["name"]
        #     currentItem["price"] = updatedItem["price"]
            
        #     print(currentItem)
        #     return {"message":"Item Updated"}
        # except:
        #     abort(404,message="Item not Found/Deleted")


      ### After the Integration of the Database ###

      # Put Method -- if the id is not found then it will create the new item with that ID that we are passing.

      item = ItemModel.query.get(item_id)
    
      if item:
         item.price = updatedItem["price"]
         item.name = updatedItem["name"]
      else:

         # This will give me a Integrity Not Null Error
         item = ItemModel(id=item_id,**updatedItem)

      db.session.add(item)
      db.session.commit()
      
      return item

@blp.route("/item")
class Item(MethodView):
    @jwt_required() ### This is required for the JWT authorization
    @blp.response(200,ItemSchema(many=True))
    def get(self):
       # return {"item":list(items.values())}
       # return items.values()

       return ItemModel.query.all()

    
    @jwt_required(fresh=True) ### This is required for the JWT authorization 
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,itemData):
        # itemData = request.get_json()


        # if("price" not in itemData or "store_id" not in itemData or "name" not in itemData):
        #     abort(400,message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload")

        # Checking if the Item is already present in that store or not

        # for item in items.values():
        #     if(itemData["name"] == item["name"] and itemData["store_id"] == item["store_id"]):
        #         abort(400,message="Item already exist")

        
        # Checking if the Store is present or not before adding the items 

        # if itemData["store_id"] not in stores:
        #     abort(404,message="Store not Found") 
            
        # item_id = uuid.uuid4().hex

        # new_item = {
        #     **itemData, # This will make the value inside the storeData in a key value pair
        #     "id":item_id
        # }

        # items[item_id] = new_item


        ### After the Integration of the Database ###

        print(itemData)
        item = ItemModel(**itemData)
        print(item)

        try:
           db.session.add(item)
           db.session.commit()
        except:
           abort(400,message = "Cannot add Data to the Database")

        return item

        
    




