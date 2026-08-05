# menu/auth.py
import sys
import os

# Ajouter le chemin du projet
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models import Utilisateur


class Auth:
    """Gère l'authentification des utilisateurs"""

    def __init__(self, db):
        self.db = db
        self.utilisateur_connecte = None

    def login(self):
        """Authentifie un utilisateur"""
        print("\n" + "=" * 50)
        print("AUTHENTIFICATION")
        print("=" * 50)

        login = input("Login: ")
        mot_de_passe = input("Mot de passe: ")

        try:
            utilisateur = Utilisateur.authentifier(self.db, login, mot_de_passe)
            if utilisateur:
                self.utilisateur_connecte = utilisateur
                print(f"\n Bonjour {utilisateur.prenom} {utilisateur.nom}!")
                print(f"   Rôle: {utilisateur.role}")
                return True
            else:
                print("\n Login ou mot de passe incorrect.")
                return False
        except Exception as e:
            print(f"\n Erreur lors de l'authentification: {e}")
            return False

    def logout(self):
        """Déconnecte l'utilisateur"""
        if self.utilisateur_connecte:
            print(f"\n Au revoir {self.utilisateur_connecte.prenom} {self.utilisateur_connecte.nom}!")
            self.utilisateur_connecte = None
        else:
            print("\n Vous n'êtes pas connecté.")

    def est_connecte(self):
        return self.utilisateur_connecte is not None

    def get_utilisateur_connecte(self):
        return self.utilisateur_connecte

    def est_admin(self):
        return self.est_connecte() and self.utilisateur_connecte.role == "ADMIN"

    def est_technicien(self):
        return self.est_connecte() and self.utilisateur_connecte.role == "TECHNICIEN"

    def est_utilisateur(self):
        return self.est_connecte() and self.utilisateur_connecte.role == "UTILISATEUR"

    def afficher_info_utilisateur(self):
        if self.est_connecte():
            u = self.utilisateur_connecte
            print("\n" + "-" * 50)
            print("INFORMATIONS UTILISATEUR")
            print("-" * 50)
            print(f"ID: {u.id}")
            print(f"Login: {u.login}")
            print(f"Nom: {u.nom}")
            print(f"Prénom: {u.prenom}")
            print(f"Email: {u.email}")
            print(f"Rôle: {u.role}")
            print(f"Service: {u.service or '-'}")
            print(f"Date création: {u.date_creation}")
        else:
            print("\n Aucun utilisateur connecté.")

    def changer_mot_de_passe(self):
        if not self.est_connecte():
            print("\n Vous devez être connecté pour changer votre mot de passe.")
            return

        print("\n" + "-" * 50)
        print("CHANGEMENT DE MOT DE PASSE")
        print("-" * 50)

        ancien_mdp = input("Ancien mot de passe: ")
        nouveau_mdp = input("Nouveau mot de passe: ")
        confirmation = input("Confirmer le nouveau mot de passe: ")

        if nouveau_mdp != confirmation:
            print("\n Les mots de passe ne correspondent pas.")
            return

        utilisateur = Utilisateur.authentifier(
            self.db,
            self.utilisateur_connecte.login,
            ancien_mdp
        )

        if not utilisateur:
            print("\n Ancien mot de passe incorrect.")
            return

        try:
            self.utilisateur_connecte.password = nouveau_mdp
            self.utilisateur_connecte.sauvegarder(self.db)
            print("\n Mot de passe changé avec succès!")
        except Exception as e:
            print(f"\n Erreur lors du changement de mot de passe: {e}")