import sqlite3
from flask_restful import reqparse, Resource
from models.user import UserModel


class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Please enter username")
    parser.add_argument('password', type=str, required=True, help="please enter password")

    def post(self):
        data = UserRegistration.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User already exist"}
        user = UserModel(**data)

        return {'message': "User created successfully"}, 201
