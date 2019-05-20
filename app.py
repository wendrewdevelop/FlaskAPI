from flask import Flask, jsonify
from flask_restful import Api

from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from configs.BDConfig import banco
from configs.blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///configs/banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'SHIIIIIIIUBEQUIETDONTTELLANYONE'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)
banco.init_app(app)

@app.before_first_request
def newBD():
   banco.create_all()

@jwt.token_in_blacklist_loader
def verifyBlacklist(token):
   return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def AccessTokenInvalidated():
   return jsonify({'message': 'Você foi deslogado.'}), 401

api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<int:id>')
api.add_resource(User, '/usuarios/<int:id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
   app.run(debug = True)