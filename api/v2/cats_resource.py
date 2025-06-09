from flask import jsonify
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.cats import Cats
from data.shelters import Shelters

parser = reqparse.RequestParser()
parser.add_argument('cats_id', required=False, type=int)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('breed', required=False)
parser.add_argument('features', required=False)
parser.add_argument('shelters_id', required=True, type=int)


# Проверка, что кот существует
def abort_if_cats_not_found(cats_id):
    session = db_session.create_session()
    cats = session.query(Cats).get(cats_id)
    if not cats:
        abort(404, message=f"Cats {cats_id} not found")


# Проверка, что приют существует
def abort_if_shelters_not_found(shelters_id):
    session = db_session.create_session()
    shelters = session.query(Shelters).get(shelters_id)
    if not shelters:
        abort(404, message=f"Shelters {shelters_id} not found")


# Проверка, что приют подтверждён
def abort_if_shelters_not_validated(shelters_id):
    session = db_session.create_session()
    shelters = session.query(Shelters).get(shelters_id)
    if not shelters.validated:
        abort(404, message=f"Shelters {shelters_id} is not validated")


# Класс для работ с одним котом
class CatsResource(Resource):
    def get(self, cats_id):
        abort_if_cats_not_found(cats_id)
        session = db_session.create_session()
        cats = session.query(Cats).get(cats_id)
        return jsonify({'cats': cats.to_dict(
            only=('name', 'age', 'breed'))})

    def delete(self, cats_id):
        abort_if_cats_not_found(cats_id)
        session = db_session.create_session()
        cats = session.query(Cats).get(cats_id)
        session.delete(cats)
        session.commit()
        return jsonify({'success': 'OK'})


# Класс для рабрты со всеми котами
class CatsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        cats = session.query(Cats).all()
        return jsonify({'cats': [item.to_dict(
            only=('name', 'age', 'breed', 'features', 'shelter_id')) for item in cats]})

    def post(self):
        args = parser.parse_args()
        abort_if_shelters_not_found(args['shelters_id'])
        abort_if_shelters_not_validated(args['shelters_id'])
        session = db_session.create_session()
        cat = Cats()
        if 'name' in args:
            cat.name = args['name']
        if 'age' in args:
            cat.age = args['age']
        if 'breed' in args:
            cat.breed = args['breed']
        if 'features' in args:
            cat.features = args['features']
        if 'shelter_id' in args:
            cat.shelter_id = args['shelter_id']
        session.add(cat)
        session.commit()
        return jsonify({'success': 'OK'})
