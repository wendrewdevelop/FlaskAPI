from flask_restful import Resource, reqparse
from models.Usuario import UserModel
from configs.blacklist import BLACKLIST
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp


argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type = str, required = True, help = 'O campo "login" não pode ficar em branco.')
argumentos.add_argument('senha', type = str, required = True, help = 'O campo "senha" não pode ficar em branco.')

class User(Resource):
   #/usuarios/{user_id}
   def get(self, id):
      user = UserModel.findUser(id)
      if user:
         return user.json()
      
      return {'message': 'Usuário não encontrado!'}, 404 #Not Found.

   @jwt_required
   def delete(self, id):
      user = UserModel.findUser(id)
      if user:
         try:
            user.deleteUser()
         except:
            return {'message': 'Ocorreu um erro interno ao tentar deletar o registro.'}, 500
         return {'message': 'Usuário deletado!'}
      return {'message': 'Usuário não encontrado'}, 404   

class UserRegister(Resource):
   #/cadastro
   def post(self):
      dados = argumentos.parse_args()

      if UserModel.findByLogin(dados['login']):
         return {'message': "O login '{}' ja existe!".format(dados['login'])}
      
      user = UserModel(**dados)
      user.saveUser()

      return {'message': 'Usuário criado com sucesso!'}, 201

class UserLogin(Resource):
   @classmethod
   def post(cls):
      dados = argumentos.parse_args()

      user = UserModel.findByLogin(dados['login'])

      if user and safe_str_cmp(user.senha, dados['senha']):
         AccessToken = create_access_token(identity = user.id)
         return {'AccessToken': AccessToken}, 200
      return {'message': 'Usuário ou senha incorreto.'}, 401 #Não autorizado.

class UserLogout(Resource):
   @jwt_required
   def post(self):
      jwt_id = get_raw_jwt()['jti'] #JWT Token identificador
      BLACKLIST.add(jwt_id)
      return {'message': 'Deslogado!'}, 200
