from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.accounts import account_bank

from mongoengine.errors import FieldDoesNotExist, \
NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

# from resources.errors import SchemaValidationError, AccountNumberAlreadyExistsError, EmailAlreadyExistsError, \
# InternalServerError, UpdatingAccountError, DeletingAccountError, AccountNotExistsError, UnauthorizedError

account_blueprint = Blueprint('accounts', __name__)

#  get account bank
@account_blueprint.route('/get_accounts')
@jwt_required
def get_accounts():
    accounts = account_bank.objects().to_json()
    return Response(accounts, mimetype="application/json", status=200)

@account_blueprint.route('/add_account', methods=['POST'])
@jwt_required
def add_account():
    try:
        getjwt = get_jwt_identity()
        role = getjwt['role']
        if role == 'admin':
          body = request.get_json()
          acc_bank = account_bank(**body).save()
          id = acc_bank.id
          return {'id': str(id), 'message': str('Add account successfully'), 'status' : 200 }, 200
        else:
          return { 'message' : str('Not permission'), 'status' : 401 }, 401
    except (FieldDoesNotExist, ValidationError):
      return { 'message' : str('Request is missing required fields'), 'status' : 400 }, 400
    except NotUniqueError:
      return { 'message' : str('Account number already exists'), 'status' : 400 }, 400
    except Exception:
      return { 'message' : str('Something went wrong'), 'status' : 500 }, 500


@account_blueprint.route('/update_account/<id>', methods=['PUT'])
@jwt_required
def update_account(id):
    try:
      getjwt = get_jwt_identity()
      role = getjwt['role']
      if role == 'admin':
        body = request.get_json()
        account_bank.objects.get(id=id).update(**body)
        return { 'message' : str('Update account successfully'), 'status' : 200 }, 200
      else:
        return { 'message' : str('Not permission'), 'status' : 401 }, 401
    except InvalidQueryError:
      return { 'message' : str('Request is missing required fields'), 'status' : 400 }, 400
    except DoesNotExist:
      return { 'message' : str('Updating account added by other is forbidden'), 'status' : 403 }, 403
    except Exception:
      return { 'message' : str('Something went wrong'), 'status' : 500 }, 500

@account_blueprint.route('/delete_account/<id>', methods=['DELETE'])
@jwt_required
def delete_account(id):
    try:
      getjwt = get_jwt_identity()
      role = getjwt['role']
      if role == 'admin':
        account_bank.objects.get(id=id).delete()
        return { 'message' : str('Delete account successfully'), 'status': 200}, 200
      else:
        return { 'message' : str('Not permission'), 'status' : 401 }, 401 
    except DoesNotExist:
      return { 'message' : str('Deleting account added by other is forbidden'), 'status' : 403 }, 403
    except Exception:
      return { 'message' : str('Something went wrong'), 'status' : 500 }, 500


# @account_blueprint.route('/search_account/<keyword>')
# @jwt_required
# def search_account(keyword):
#   return Response(kkk, mimetype="application/json", status=200)
    