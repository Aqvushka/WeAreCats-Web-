from flask import jsonify
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.users import Users
from data.shelters import Shelters

parser = reqparse.RequestParser()
parser.add_argument('shelters_id', required=False, type=int)
parser.add_argument('name', required=True)
parser.add_argument('phone', required=False)
parser.add_argument('address', required=False)
parser.add_argument('validated', required=False)
parser.add_argument('user_id', required=True, type=int)


# Проверка, что приют существует
def abort_if_shelters_not_found(shelters_id):
    session = db_session.create_session()
    shelters = session.query(Shelters).get(shelters_id)
    if not shelters:
        abort(404, message=f"Shelters {shelters_id} not found")


# Проверка, что пользователь существует
def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    users = session.query(Users).get(user_id)
    if not users:
        abort(404, message=f"Users {user_id} not found")


# Класс для работы с одним приютом
class SheltersResource(Resource):
    def get(self, shelters_id):
        abort_if_shelters_not_found(shelters_id)
        session = db_session.create_session()
        shelters = session.query(Shelters).get(shelters_id)
        return jsonify({'shelters': shelters.to_dict(
            only=('name', 'phone', 'address'))})

    def delete(self, shelters_id):
        abort_if_shelters_not_found(shelters_id)
        session = db_session.create_session()
        shelters = session.query(Shelters).get(shelters_id)
        session.delete(shelters)
        session.commit()
        return jsonify({'success': 'OK'})


# Класс для работы со всеми приютами
class SheltersListResource(Resource):
    def get(self):
        shelters = db_session.create_session().query(Shelters).filter(Shelters.validated == 0)
        return jsonify({'shelters': [item.to_dict(
            only=('id', 'name', 'phone', 'address', 'validated', 'user_id')) for item in shelters]})

    def post(self):
        args = parser.parse_args()
        abort_if_users_not_found(args['user_id'])
        session = db_session.create_session()
        shelters = Shelters()
        if 'name' in args:
            shelters.name = args['name']
        if 'phone' in args:
            shelters.phone = args['phone']
        if 'address' in args:
            shelters.address = args['address']
        if 'validated' in args:
            shelters.validated = args['validated']
        if 'user_id' in args:
            shelters.user_id = args['user_id']
            user = session.query(Users).get(int(args['user_id'])) #Если пользователь не был приютом - станет им
            user.is_shelter = 1
        session.add(shelters)
        session.commit()
        return jsonify({'success': 'OK'})
