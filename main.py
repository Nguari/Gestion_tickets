from menu.interface import Interface


def afficher_titre():
    print("\n" + "#" * 60)
    print(" " * 15 + "SYSTÈME DE GESTION DE TICKETS")
    print("#" * 60)


def authentifier(app):
    """Force la connexion avant d'accéder à quoi que ce soit"""
    tentatives_max = 3
    tentatives = 0

    while tentatives < tentatives_max:
        connecte = app.auth.login()
        if connecte:
            return True
        tentatives += 1
        restantes = tentatives_max - tentatives
        if restantes > 0:
            print(f"Il vous reste {restantes} tentative(s).\n")
        else:
            print("\n Trop de tentatives échouées.")

    return False


def menu_role_utilisateur(app):
    while True:
        print("\n" + "=" * 50)
        print(f"MENU UTILISATEUR - {app.auth.get_utilisateur_connecte().prenom}")
        print("=" * 50)
        print("1. Créer un incident")
        print("2. Voir mes tickets")
        print("3. Mon compte")
        print("0. Déconnexion")

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            app.creer_incident()
        elif choix == "2":
            app.voir_mes_tickets()
        elif choix == "3":
            app.menu_mon_compte()
            if not app.auth.est_connecte():
                break
        elif choix == "0":
            app.auth.logout()
            break
        else:
            print("\n Choix invalide.")


def menu_role_technicien(app):
    while True:
        print("\n" + "=" * 50)
        print(f"MENU TECHNICIEN - {app.auth.get_utilisateur_connecte().prenom}")
        print("=" * 50)
        print("1. Lister les incidents")
        print("2. Rechercher un incident")
        print("3. Ajouter une intervention")
        print("4. Lister mes interventions")
        print("5. Changer le statut d'un incident")
        print("6. Mon compte")
        print("0. Déconnexion")

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            app.lister_incidents()
        elif choix == "2":
            app.rechercher_incident()
        elif choix == "3":
            app.ajouter_intervention()
        elif choix == "4":
            app.rechercher_intervention()  # option "3. Par Technicien"
        elif choix == "5":
            app.changer_statut_incident()
        elif choix == "6":
            app.menu_mon_compte()
            if not app.auth.est_connecte():
                break
        elif choix == "0":
            app.auth.logout()
            break
        else:
            print("\n Choix invalide.")


def menu_role_admin(app):
    while True:
        print("\n" + "=" * 50)
        print(f"MENU ADMIN - {app.auth.get_utilisateur_connecte().prenom}")
        print("=" * 50)
        print("1. Gestion des utilisateurs")
        print("2. Gestion des incidents")
        print("3. Gestion des interventions")
        print("4. Statistiques")
        print("5. Mon compte")
        print("0. Déconnexion")

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            app.menu_utilisateurs()
        elif choix == "2":
            app.menu_incidents()
        elif choix == "3":
            app.menu_interventions()
        elif choix == "4":
            app.afficher_statistiques()
        elif choix == "5":
            app.menu_mon_compte()
            if not app.auth.est_connecte():
                break
        elif choix == "0":
            app.auth.logout()
            break
        else:
            print("\n Choix invalide.")


def rediriger_vers_menu(app):
    """Envoie l'utilisateur vers le menu correspondant à son rôle"""
    utilisateur = app.auth.get_utilisateur_connecte()

    if app.auth.est_admin():
        menu_role_admin(app)
    elif app.auth.est_technicien():
        menu_role_technicien(app)
    elif app.auth.est_utilisateur():
        menu_role_utilisateur(app)
    else:
        print(f"\n Rôle inconnu : {utilisateur.role}")


def main():
    afficher_titre()

    app = Interface()

    try:
        if not authentifier(app):
            print("\nFin du programme.")
            return

        while app.auth.est_connecte() or authentifier(app):
            rediriger_vers_menu(app)
            if not app.auth.est_connecte():
                continuer = input("\nSe reconnecter ? (o/n) : ").strip().lower()
                if continuer != 'o':
                    break

        print("\nÀ bientôt !")

    finally:
        app.db.fermer()


if __name__ == "__main__":
    main()