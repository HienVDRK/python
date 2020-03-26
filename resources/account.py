from flask import Blueprint, Response, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.accounts import account_bank
import json

from mongoengine.errors import FieldDoesNotExist, \
NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from .extentions import mongo

account_blueprint = Blueprint('accounts', __name__)


#  search account bank
@account_blueprint.route('/accounts1')
def searchAccount():
  accounts = mongo.db.account_bank
  query_params = request.args
  output = []
  page_size = int(query_params.get('page_size'))
  page_index = int(query_params.get('page_index'))
  skips = page_size * page_index
  order_by = query_params.get('order_by')
  order_direction = int(query_params.get('order_direction'))
  query = json.loads(query_params.get('query'))

  data = accounts.find(query).sort(order_by, order_direction).skip(skips).limit(page_size)
  total = data.count()
  for account in data:
    output.append({
      'account_number': account['account_number'], 'balance': account['balance'], 'firstname' : account['firstname'], "lastname" : account['lastname'],
      'age' : account['age'], 'gender' : account['gender'], 'address' : account['address'], 'employer' : account['employer'],
      'email' : account['email'], 'city' : account['city'], 'state' : account['state']
    })
  return jsonify({
    'success': "true",
    'data': output,
    'total': total,
    'page_size': page_size,
    'page_index': page_index
  })

#  get account bank
@account_blueprint.route('/accounts')
# @jwt_required
def get_accounts():
    accounts = account_bank.objects().to_json()
    return Response(accounts, mimetype="application/json", status=200)
  

@account_blueprint.route('/accounts/<id>')
# @jwt_required
def get_accounts_by_id(id):
  print(id)
  accounts = account_bank.objects.get(account_number=id).to_json()
  return accounts 

@account_blueprint.route('/accounts', methods=['POST'])
@jwt_required
def add_account():
    try:
        getjwt = get_jwt_identity()
        role = getjwt['role']
        if role == 'admin':
          body = request.get_json()
          print('add', body)
          acc_bank = account_bank(**body).save()
          id = acc_bank.id
          return {
            'id': str(id),
            'message': str('Add account successfully'),
            'status' : 200 
          }, 200
        else:
          return {
            'message' : str('Not permission'),
            'status' : 401 
          }, 401
          
    except (FieldDoesNotExist, ValidationError):
      return { 
        'message' : str('Request is missing required fields'),
        'status' : 400 
      }, 400
      
    except NotUniqueError:
      body = request.get_json()
      account = account_bank.objects(account_number=body['account_number'])
      email = account_bank.objects(email=body['email'])
      if account:
        return {
          'message' : str('Account number already exists'),
          'status' : 400 
        }, 400
      elif email:
        return {
          'message' : str('Email already exists'),
          'status' : 400 
        }, 400
      
    except Exception:
      return {
        'message' : str('Something went wrong'),
        'status' : 500 
      }, 500


@account_blueprint.route('/accounts/<id>', methods=['PUT'])
@jwt_required
def update_account(id):
    try:
      getjwt = get_jwt_identity()
      role = getjwt['role']
      if role == 'admin':
        body = request.get_json()
        account_bank.objects.get(account_number=id).update(**body)
        return {
          'message' : str('Update account successfully'),
          'status' : 200 
        }, 200
        
      else:
        return {
          'message' : str('Not permission'),
          'status' : 401 
        }, 401
        
    except InvalidQueryError:
      return {
        'message' : str('Request is missing required fields'),
        'status' : 400 
      }, 400
      
    except DoesNotExist:
      return {
        'message' : str('Updating account added by other is forbidden'),
        'status' : 403
      }, 403
      
    except Exception:
      return {
        'message' : str('Something went wrong'),
        'status' : 500 
      }, 500

@account_blueprint.route('/accounts/<id>', methods=['DELETE'])
@jwt_required
def delete_account(id):
    try:
      getjwt = get_jwt_identity()
      role = getjwt['role']
      if role == 'admin':
        account_bank.objects.get(account_number=id).delete()
        return {
          'message' : str('Delete account successfully'),
          'status': 200
        }, 200
        
      else:
        return {
          'message' : str('Not permission'),
          'status' : 401 
        }, 401 
        
    except DoesNotExist:
      return {
        'message' : str('Deleting account added by other is forbidden'),
        'status' : 403 
      }, 403
      
    except Exception:
      return {
        'message' : str('Something went wrong'),
        'status' : 500 
      }, 500


# @account_blueprint.route('/search_account/<keyword>')
# @jwt_required
# def search_account(keyword):
#   return Response(kkk, mimetype="application/json", status=200)
    