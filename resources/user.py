from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 # Hashing Algorithm
from flask_jwt_extended import create_access_token,create_refresh_token,get_jwt,get_jwt_identity,jwt_required


from db import db
from models.user import UserModel
from schema import UserSchema

from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        
        getData = UserModel.query.filter_by(username = user_data["username"]).first()
        
        if getData:
           abort(409, message="A user with that username already exists.")

        # if UserModel.query.filter(UserModel.username == user_data["username"]).first():
        
        username=user_data["username"]
        password=pbkdf2_sha256.hash(user_data["password"]) # hashing the Password

        user = UserModel(username=username,password=password)

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201
    


### This is Just for the Testing Purpose ###


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):

        user = UserModel.query.filter_by(username=user_data["username"]).first()
     

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token,"refresh_token":refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        print(get_jwt())
        jti = get_jwt().jti
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
      
                
@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design


        ### From here the token that we will get will be a refresh token not a fresh token. ###

        ### This will add the refresh token to the bloclist and we can use that refresh that refresh token untill that has been expired after that we cannot use that token ###

        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200