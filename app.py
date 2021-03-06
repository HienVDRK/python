#~project_anm/app.py

from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from resources.extentions import mongo
from flask_cors import CORS

from database.db import initialize_db
from resources.auth import user_blueprint
from resources.account import account_blueprint

app = Flask(__name__)
CORS(app)

app.config.from_envvar('ENV_FILE_LOCATION')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/project_anm'
}
# --pymongo
app.config["MONGO_URI"] = "mongodb://localhost/project_anm"
mongo.init_app(app)
# end--pymongo

initialize_db(app)

app.register_blueprint(user_blueprint, url_prefix='/auth')
app.register_blueprint(account_blueprint, url_prefix='/account')

app.run()