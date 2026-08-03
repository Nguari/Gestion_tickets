from database import Connexion
from models import Utilisateur

def welcome(utilisateur):
    print("\n" + "=" * 40)
    print(f"Bienvenue ({utilisateur.prenom} {utilisateur.nom}) !!!")
    print(f"Rôle : {utilisateur.role}")
    print(f"Service : {utilisateur.service}")
    print("=" * 40)

def auht(db):
    print(" +++++++++Connexion++++++++++")
    tentatives_max = 3
    tentatives = 0

    while tentatives < tentatives_max:
        login = input("Entrer le login : ")
        password = input("Entrer le mot de passe : ")

        utilisateur = Utilisateur.authentifier(db,login, password)

        if utilisateur :
            return utilisateur
        else:
            tentatives += 1
            rest = tentatives_max - tentatives
            if rest > 0:
                print("Mot de passe ou login incorrect veuillez réessayer !!!")
                print(f"Il vous reste {rest} tentatives")
            else :
                print("Trop de tentatives échouée fermeture du programme !!!!")
    return None

def main():
    with Connexion() as db:
        if db.connection is None:
            print("Erreur lors de la connexion !")
            return

        utilisateur = auht(db)
        if utilisateur :
            welcome(utilisateur)
        else:
            print("Fin du programme !")

if __name__ == "__main__":
    main()