# Marshamallow helps us in the Validating the data but only the "Incoming Data"

# It returns the Validated Dictionary after Verfying the client request from the client


from marshmallow import Schema, fields


# class ItemSchema(Schema):
#     id = fields.Str(dump_only=True)
#     name = fields.Str(required=True)
#     price = fields.Float(required=True)
#     store_id = fields.Str(required=True)



# # When we are updating the Item

# class ItemUpdateSchema(Schema):
#     name = fields.Str()
#     price = fields.Float()



# # When we are creating the Store


# class StoreSchema(Schema):
#     id = fields.Str(dump_only=True)
#     name = fields.Str(required=True)


# # For Response Schema

# class ResponseSchema(Schema):
#     message = fields.Str(dump_only=True)


## dump_only = At response time
## load_only = At request time


from marshmallow import Schema, fields


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Str()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)



class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True,load_only=True)


class UserRegisterSchema(UserSchema):
    useremail = fields.Str(required=True)

