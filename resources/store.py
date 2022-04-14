from flask_restful import Resource
from models.store import StoreModel
from db import db


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 400

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "Store already exist"},400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred"}, 500
        return store.json(),201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete()

        return {"message": "Deleted"}


class StoreList(Resource):
    def get(self):
        return {"store": [store.json() for store in StoreModel.query.all()]}