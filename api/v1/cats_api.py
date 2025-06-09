from flask import Blueprint, jsonify, request

from data import db_session
from data.cats import Cats
from data.shelters import Shelters

blueprint = Blueprint('cats_api', __name__,
                      template_folder='templates')

#Получение всех котов
@blueprint.route('/api/cats', methods=['GET'])
def get_cats():
    cats = db_session.create_session().query(Cats).all()
    return jsonify(
        {
            'cats':
                [item.to_dict(only=('name', 'age', 'breed', 'features'))
                 for item in cats]
        }
    )


#Возвращение информации об одном коте
@blueprint.route('/api/cats/<int:cats_id>', methods=['GET'])
def get_one_cat(cats_id):
    cat = db_session.create_session().query(Cats).get(cats_id)
    if not cat:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'cat': cat.to_dict(only=
                               ('name', 'age', 'breed', 'features'))
        }
    )


#Создание кота
@blueprint.route('/api/cats', methods=['POST'])
def create_cat():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': '404'})
    elif not all(key in request.json for key in
                 ['name', 'shelter_id']):
        return jsonify({'error': '206'})
    elif all(key in request.json for key in ['id']):
        return jsonify({'error': 'You cant specify id'})
    elif not session.query(Shelters).filter(Shelters.id == request.json['shelter_id']).first():
        return jsonify({'error': '404 (Shelter is not found)'})
    elif not session.query(Shelters).filter(Shelters.id == request.json['shelter_id']).first().validated:
        return jsonify({'error': 'Shelter is not validated'})
    cat = Cats(
        name=request.json['name'],
        shelter_id=request.json['shelter_id']
    )
    if 'age' in request.json:
        cat.age = request.json['age']
    if 'breed' in request.json:
        cat.breed = request.json['breed']
    if 'features' in request.json:
        cat.features = request.json['features']
    session.add(cat)
    session.commit()
    return jsonify({'cats': 'created'})


#Удаление кота
@blueprint.route('/api/cats/<int:cats_id>', methods=['DELETE'])
def delete_cats(cats_id):
    session = db_session.create_session()
    cat = session.query(Cats).get(cats_id)
    if not cat:
        return jsonify({'error': '404'})
    session.delete(cat)
    session.commit()
    return jsonify({'cat': 'deleted'})


#Изменение кота
@blueprint.route('/api/cats/<int:cats_id>', methods=['PUT'])
def refactor_cats(cats_id):
    session = db_session.create_session()
    if not session.query(Cats).filter(Cats.id == cats_id).first():
        return jsonify({'error': '404'})
    elif 'shelter_id' in request.json:
        if not session.query(Shelters).filter(Shelters.id == request.json['shelter_id']).first():
            return jsonify({'error': '404 (Shelter is not found)'})
    elif all(key in request.json for key in ['id']):
        return jsonify({'error': 'You cant specify id'})
    elif not session.query(Shelters).filter(Shelters.id == request.json['shelter_id']).first().validated:
        return jsonify({'error': 'Shelter is not validated'})
    cat = session.query(Cats).get(cats_id)
    if not (any(key in request.json for key in ['name', 'age', 'breed', 'features', 'shelter_id'])):
        return jsonify({'error': '400'})
    if 'name' in request.json:
        cat.name = request.json['name']
    if 'age' in request.json:
        cat.age = request.json['age']
    if 'breed' in request.json:
        cat.breed = request.json['breed']
    if 'features' in request.json:
        cat.features = request.json['features']
    if 'shelter_id' in request.json:
        cat.shelter_id = request.json['shelter_id']
    session.commit()
    session.close()
    return jsonify({'cat': 'refactored'})
