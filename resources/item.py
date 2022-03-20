#import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
class Item(Resource): ##resources should only have methods client interacts with
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank.")

    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'Item not found.'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An Item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the iterm.'}, 500 #internal server error

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name): ##needs to be idempotent, doesn't change if the same

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, data['price'], data['store_id']) #can do **data for simplicity

        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} ##would use map and lambda function if looking for less pythonic code for other readers