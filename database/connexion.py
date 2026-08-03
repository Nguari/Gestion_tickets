import mysql.connector
from mysql.connector import Error
from .config import Config


class Connexion:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connecter(self):
        try:
            self.connection = mysql.connector.connect(
                host=Config.HOST,
                user=Config.USER,
                password=Config.PASSWORD,
                database=Config.DATABASE,
                port=Config.PORT
            )
            self.cursor = self.connection.cursor()
            print(" Connexion à la base réussie")
            return self.connection
        except Error as e:
            print(f" Erreur lors de la connexion : {e}")
            return None

    def executer(self, requete, valeurs=None):
        try:
            self.cursor.execute(requete, valeurs or ())
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            print(f" Erreur d'exécution : {e}")
            self.connection.rollback()

    def selectionner(self, requete, valeurs=None):
        try:
            self.cursor.execute(requete, valeurs or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f" Erreur de sélection : {e}")
            return []

    def fermer(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Connexion fermée")


    def __enter__(self):
        self.connecter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.fermer()