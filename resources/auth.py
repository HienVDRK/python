from flask import Blueprint, Response, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database.users import User
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
import json

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/users_signup', methods=['POST'])
def sign_up():
    body = request.get_json()
    user = User(**body)
    user.password = generate_password_hash(user.password).decode('utf8')
    user.save()
    id = user.id
    return {'id': str(id)}, 200


@user_blueprint.route('/users_login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.objects.get(email=body.get('email'))
    authorized = check_password_hash(user.password, body.get('password'))
    if not authorized:
        return {'error': 'Email or password invalid'}, 401
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=({ 
        'role' : user['role'],
        'username' : user['username']}), expires_delta=expires)
    return {'token': access_token}, 200 
    

@user_blueprint.route('/users')
@jwt_required
def get_users():
    users = User.objects().to_json()
    return Response(users, mimetype="application/json", status=200)
    

@user_blueprint.route('/users/<id>')
@jwt_required
def get_user(id):
    user = User.objects.get(id=id).to_json()
    return Response(user, mimetype="application/json", status=200) 


# @user_blueprint.route('/users', methods=['POST'])
# @jwt_required
# def add_user():
#     body = request.get_json()
#     user = User(**body)
#     user.password = generate_password_hash(user.password).decode('utf8')
#     user.save()
#     id = user.id
#     return {'id': str(id)}, 200

# @jwt_required
# @user_blueprint.route('/users/<id>', methods=['PUT'])
# def update_user(id):
#     body = request.get_json()
#     User.objects.get(id=id).update(**body)
#     return '', 200

# @jwt_required
# @user_blueprint.route('/users/<id>', methods=['DELETE'])
# def delete_user(id):
#     User.objects.get(id=id).delete()
#     return '', 200      