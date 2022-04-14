import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be empty")
    parser.add_argument('store_id', type=int, required=True, help="This field cannot be empty")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_username(name)
        if item:
            return item.json()
        return {"message": "Item not found"}

    def post(self, name):
        if ItemModel.find_by_username(name):
            return {'message': "Item {} already exist".format(name)}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except Exception as e:
            return {"message":"An error occurred"}, 500
        return item, 201

    def delete(self, name):
        item = ItemModel.find_by_username(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_username(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

