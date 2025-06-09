from flask import Blueprint, jsonify, request

from data import db_session
from data.users import Users
from data.shelters import Shelters
from data.cats import Cats

blueprint = Blueprint('shelters_api', __name__,
                      template_folder='templates')


# Получение всех приютов
@blueprint.route('/api/shelters', methods=['GET'])
def get_shelters():
    shelters = db_session.create_session().query(Shelters).filter(Shelters.validated == 1)
    return jsonify(
        {
            'shelters':
                [item.to_dict(only=('name', 'address', 'phone'))
                 for item in shelters]
        }
    )


#Получение котов одного приюта
@blueprint.route('/api/shelters/<int:shelters_id>', methods=['GET'])
def get_one_shelter(shelters_id):
    shelter = db_session.create_session().query(Shelters).get(shelters_id)
    cats = shelter.cats
    if not shelter:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'cats': [item.to_dict(only=('id', 'name', 'age', 'breed', 'features'))
                     for item in cats]
        }
    )


#Создание приюта
@blueprint.route('/api/shelters', methods=['POST'])
def create_shelter():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': '404'})
    elif not all(key in request.json for key in
                 ['name', 'address', 'phone', 'user_id', 'validated']):
        return jsonify({'error': '206'})
    elif all(key in request.json for key in ['id']):
        return jsonify({'error': 'You cant specify id'})
    elif not session.query(Users).filter(Users.id == request.json['user_id']).first():
        return jsonify({'error': '404 (User is not found)'})
    shelter = Shelters(
        name=request.json['name'],
        address=request.json['address'],
        phone=request.json['phone'],
        user_id=request.json['user_id'],
        validated=request.json['validated']
    )
    session.add(shelter)
    session.commit()
    return jsonify({'shelter': 'created'})


#Удаление приюта
@blueprint.route('/api/shelters/<int:shelters_id>', methods=['DELETE'])
def delete_shelter(shelters_id):
    session = db_session.create_session()
    shelter = session.query(Shelters).get(shelters_id)
    if not shelter:
        return jsonify({'error': '404'})
    session.delete(shelter)
    session.commit()
    return jsonify({'shelter': 'deleted'})


# Изменение приюта
@blueprint.route('/api/shelters/<int:shelters_id>', methods=['PUT'])
def refactor_shelter(shelters_id):
    session = db_session.create_session()
    if not session.query(Shelters).filter(Shelters.id == shelters_id).first():
        return jsonify({'error': '404'})
    elif all(key in request.json for key in ['id']):
        return jsonify({'error': 'You cant specify id'})
    elif 'user_id' in request.json:
        if not session.query(Users).filter(Users.id == request.json['user_id']).first():
            return jsonify({'error': '404 (User is not found)'})
    shelter = session.query(Shelters).get(shelters_id)
    if not (any(key in request.json for key in ['name', 'address', 'phone', 'user_id', 'validated'])):
        return jsonify({'error': '400'})
    if 'name' in request.json:
        shelter.name = request.json['name']
    if 'address' in request.json:
        shelter.address = request.json['address']
    if 'phone' in request.json:
        shelter.phone = request.json['phone']
    if 'user_id' in request.json:
        shelter.user_id = request.json['user_id']
    if 'validated' in request.json:
        shelter.validated = request.json['validated']
        user = db_session.create_session().query(Users).filter(
            Users.id == shelter.user_id).first()  # Если у приюта меняется владелец, пользователь помечается в системе как "приют"
        user.is_shelter = 1
    session.commit()
    session.close()
    return jsonify({'shelter': 'refactored'})
