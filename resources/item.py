from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import Flask, request
import sqlite3
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )
    parser.add_argument('name',
                        required=True,
                        help="Name cannot be blank"
                        )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self):
        data = Item.parser.parse_args()

        if ItemModel.find_by_name(data['name']):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        item = ItemModel(**data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    def put(self):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(data['name'])
        #updated_item = {"name": data['name], "price": data['price']}

        if item is None:
            item = ItemModel(**data)
        else:
            item.price = data["price"]
            item.name = data["name"]
            item.store_id = data["store_id"]

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}