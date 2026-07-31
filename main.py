import menu.auth

def menu_auth():
    print("Bonjour !!!!")
    compte = input("Avez vous déjà un compte?[Oui/Non] : ")
    if compte.lower() == "oui":
        login = input("Entrer votre identifiant : ")
        password = input("Entrer votre mot de passe : ")
    elif compte.lower() == "non":
        print("===========Pour créer un compte veuillez remplir les informations suivantes==============")
        nom = input("Entrer votre nom : ")
        prenom = input("Entrer votre prenom : ")
        email = input("Entrer votre identifiant electronique: ")
        servcie = input("Dans quel service êtes vous? : ")
        login = input("Créer votre identifiant : ")
        password = input("Entrer votre mot de passe : ")

menu_auth()

