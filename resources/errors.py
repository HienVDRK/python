#~/project_anm/resources/errors.py

class InternalServerError(Exception):
    pass

class SchemaValidationError(Exception):
    pass

class AccountNumberAlreadyExistsError(Exception):
    pass

class EmailAlreadyExistsError(Exception):
    pass

class UpdatingAccountError(Exception):
    pass

class DeletingAccountError(Exception):
    pass

class AccountNotExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass

errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
     "SchemaValidationError": {
         "message": "Request is missing required fields",
         "status": 400
     },
    "AccountNumberAlreadyExistsError": {
         "message": "Account number already exists",
         "status": 400
     },
      "EmailAlreadyExistsError": {
         "message": "Email address already exists",
         "status": 400
     },
     "UpdatingAccountError": {
         "message": "Updating account added by other is forbidden",
         "status": 403
     },
     "DeletingAccountError": {
         "message": "Deleting account added by other is forbidden",
         "status": 403
     },
     "AccountNotExistsError": {
         "message": "Account with given id doesn't exists",
         "status": 400
     },
     "UnauthorizedError": {
         "message": "Invalid username or password",
         "status": 401
     }
}