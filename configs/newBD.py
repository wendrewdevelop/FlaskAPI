#Criando manualmente uma base de dados e uma tabela no banco de dados SQLITE
import sqlite3

connection = sqlite3.connect('Hoteis.db')
cursor = connection.cursor()

newTable = 'CREATE TABLE IF NOT EXISTS hoteis (\
      id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,\
      nome VARCHAR(150) NOT NULL,\
      estrelas INT,\
      diaria FLOAT NOT NULL,\
      cidade VARCHAR(150)\
   )'

newHotel = "INSERT INTO hoteis VALUES (\
666, 'Teste', 5, 350.65, 'Ribeirão Preto' \
)"


cursor.execute(newTable)
cursor.execute(newHotel)
connection.commit()

connection.close()