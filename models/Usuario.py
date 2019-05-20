from configs.BDConfig import banco

class UserModel(banco.Model):
   __tablename__ = 'usuarios'

   id = banco.Column(banco.Integer(), primary_key = True)
   login = banco.Column(banco.String(50))
   senha = banco.Column(banco.String(50))

   def __init__(self, login, senha):
      self.login = login
      self.senha = senha

   def json(self):
      return {
         'id': self.id,
         'login': self.login,
         'senha': self.senha, #O retorno da senha é opção, normalmente não é retornado
      }

   @classmethod
   def findUser(cls, id):
      user = cls.query.filter_by(id = id).first()
      if user:
         return user
      return None

   @classmethod
   def findByLogin(cls, login):
      user = cls.query.filter_by(login = login).first()
      if user:
         return user
      return None

   def saveUser(self):
      banco.session.add(self)
      banco.session.commit()

   def deleteUser(self):
      banco.session.delete(self)
      banco.session.commit()