import os
import re
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
uri = os.environ.get('DATABASE_URL')

if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
if uri:
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://data.db'
app.config['SQL_DATABASE_URI']= uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.secret_key = 'wamgu'
api = Api(app)


jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

#db.init_app(app)
if __name__ == '__main__':
    app.run(debug = True)
