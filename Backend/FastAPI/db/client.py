#Encargado de la conexion con mongoDB
from pymongo import MongoClient


# Conexion a base de datos local
# db_client = MongoClient().local # con esto el cliente siempre se conecta a nuestra base en local

# Base de Datos Remoto
db_client = MongoClient(
    "mongodb+srv://landryx_db:<pasword>@clusterpython.bvwn5bo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterPython").landryx_db