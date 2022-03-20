from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    #put not needed because changing store name would be fundamentally changing everything about the store, not really an update
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json() #default is 200
        else:
            return {'message': 'Store not found.'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "Store with name '{}' already exists.".format(name)}, 400
        else:
            store = StoreModel(name)
            try:
                store.save_to_db()
            except:
                return {'message': 'An error occurred while creating the store.'}, 500

            return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        return {'message': 'Store deleted.'}

class StoreList(Resource):
    def get(self):

        return {'stores': store.json() for store in StoreModel.query.all()}