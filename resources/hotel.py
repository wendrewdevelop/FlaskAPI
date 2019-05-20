from flask_restful import Resource, reqparse
from models.Hotel import HotelModel
from flask_jwt_extended import jwt_required


class Hoteis(Resource):
   def get(self):
      return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
   argumentos = reqparse.RequestParser()
   argumentos.add_argument('nome', type = str, required = True, help = 'The field "nome" cannot be blank.')
   argumentos.add_argument('estrelas', type = int, required = True, help = 'The field "estrelas" cannot be blank.')
   argumentos.add_argument('diaria', type = float, required = True, help = 'The field "diaria" cannot be blank.')
   argumentos.add_argument('cidade', type = str, required = True, help = 'The field "cidade" cannot be blank.')

   def findHotel(id):
      for hotel in hoteis:
         if hotel['id'] == id:
            return hotel
      return None

   def get(self, id):
      hotel = HotelModel.findHotel(id)
      if hotel:
         return hotel.json()
      
      return {'message': 'Hotel não encontrado!'}, 404 #Not Found.

   @jwt_required
   def post(self, id):
      if HotelModel.findHotel(id):
         return {"message": "ID '{}', ja existe.".format(id)}, 400 #Not Found.

      dados = Hotel.argumentos.parse_args()
      hotel = HotelModel(id, **dados)
      try:
         hotel.saveHotel()
      except:
         return {'message': 'Ocorreu um erro interno ao tentar gravar o registro.'}, 500

      return hotel.json()

   @jwt_required
   def put(self, id):
      dados = Hotel.argumentos.parse_args()
      hotelFind = HotelModel.findHotel(id)
      if hotelFind:
         hotelFind.updateHotel(**dados) #Alterando hotel
         hotelFind.saveHotel()
         return hotelFind.json(), 200 #Ok
      hotel = HotelModel(id, **dados)
      try:
         hotel.saveHotel()
      except:
         return {'message': 'Ocorreu um erro interno ao tentar gravar o registro.'}, 500      
      return hotel.json(), 201

   @jwt_required
   def delete(self, id):
      hotel = HotelModel.findHotel(id)
      if hotel:
         try:
            hotel.deleteHotel()
         except:
            return {'message': 'Ocorreu um erro interno ao tentar deletar o registro.'}, 500
         return {'message': 'Hotel deletado!'}
      return {'message': 'Hotel não encontrado'}, 404   
