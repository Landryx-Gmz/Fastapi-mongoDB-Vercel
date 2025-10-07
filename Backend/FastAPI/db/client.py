#Encargado de la conexion con mongoDB
from pymongo import MongoClient

db_client = MongoClient().local # con esto el cliente siempre se conecta a nuestra base en local
