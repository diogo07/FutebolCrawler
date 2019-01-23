import mysql.connector

class Conexao:

    def __init__(self, host, user, password, database):
        self.banco = mysql.connector.connect(
            host=host,
            user=user,
            passwd=password,
            database=database
        )
