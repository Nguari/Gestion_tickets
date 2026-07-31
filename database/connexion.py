import mysql.connector
from mysql.connector import Error

try :
    conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    passwd="Nguari2006",
    database="ticketgest"
    )
    if conn.is_connected():
        print("Connection réussie !!!!")

except Error as e:
    print(f"Erreur lors de la connexion : {e}")
