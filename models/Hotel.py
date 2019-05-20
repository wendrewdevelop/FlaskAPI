from configs.BDConfig import banco

class HotelModel(banco.Model):
   __tablename__ = 'hoteis'

   id = banco.Column(banco.Integer(), primary_key = True)
   nome = banco.Column(banco.String(150))
   estrelas = banco.Column(banco.Integer())
   diaria = banco.Column(banco.Float(precision = 2))
   cidade = banco.Column(banco.String(100))

   def __init__(self, id, nome, estrelas, diaria, cidade):
      self.id = id
      self.nome = nome
      self.estrelas = estrelas
      self.diaria = diaria
      self.cidade = cidade

   def json(self):
      return {
         'id': self.id,
         'nome': self.nome,
         'estrelas': self.estrelas,
         'diaria': self.diaria,
         'cidade': self.cidade,
      }

   @classmethod
   def findHotel(cls, id):
      hotel = cls.query.filter_by(id = id).first()# SELECT * FROM hoteis WHERE id = $id
      if hotel:
         return hotel
      return None

   def saveHotel(self):
      banco.session.add(self)
      banco.session.commit()

   def updateHotel(self, nome, estrelas, diaria, cidade):
      self.nome = nome
      self.estrelas = estrelas
      self.diaria = diaria
      self.cidade = cidade

   def deleteHotel(self):
      banco.session.delete(self)
      banco.session.commit()