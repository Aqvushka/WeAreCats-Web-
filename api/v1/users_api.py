from flask import Blueprint, jsonify, request

from data import db_session
from data.users import Users

blueprint = Blueprint('users_api', __name__,
                      template_folder='templates')


# Получение всех пользователей
@blueprint.route('/api/users', methods=['GET'])
def get_users():
    users = db_session.create_session().query(Users).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'login', 'email', 'is_shelter'))
                 for item in users]
        }
    )


# Получение одного пользователя
@blueprint.route('/api/users/<int:users_id>', methods=['GET'])
def get_one_user(users_id):
    user = db_session.create_session().query(Users).get(users_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'login', 'email', 'is_shelter'))
        }
    )


# Создание пользователя
@blueprint.route('/api/users', methods=['POST'])
def create_user():
    session = db_session.create_session()
    if not request.json:
        return jsonify({'error': '404'})
    elif not all(key in request.json for key in
                 ['login', 'email', 'password']):
        return jsonify({'error': '206'})
    elif all(key in request.json for key in ['id']):
        return jsonify({'error': 'You cant specify id'})
    user = Users(
        login=request.json['login'],
        email=request.json['email']
    )
    user.set_password(request.json['password'])
    session.add(user)
    session.commit()
    return jsonify({'user': 'created'})


# Удаление пользователя
@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_user(users_id):
    session = db_session.create_session()
    user = session.query(Users).get(users_id)
    if not user:
        return jsonify({'error': '404'})
    session.delete(user)
    session.commit()
    return jsonify({'user': 'deleted'})


# Изменение пользователя
@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def refactor_user(users_id):
    session = db_session.create_session()
    if not session.query(Users).filter(Users.id == users_id).first():
        return jsonify({'error': '404'})
    elif all(key in request.json for key in ['id']):
        return jsonify({'error': 'You cant specify id'})
    user = session.query(Users).get(users_id)
    if not (any(key in request.json for key in ['login', 'email', 'password', 'is_shelter'])):
        return jsonify({'error': '400'})
    if 'login' in request.json:
        user.login = request.json['login']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'is_shelter' in request.json:
        user.is_shelter = request.json['is_shelter']
    if 'password' in request.json:
        user.set_password('password')
    session.commit()
    session.close()
    return jsonify({'user': 'refactored'})
