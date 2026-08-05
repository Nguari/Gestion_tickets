from database import Connexion
from models import Utilisateur, Incident, Intervention


def inserer_utilisateurs(db):
    """Crée des utilisateurs pour chaque rôle et plusieurs services"""
    utilisateurs_data = [
        # login, password, nom, prenom, email, role, service
        ("jdupont", "pass123", "Dupont", "Jean", "jdupont@entreprise.com", "UTILISATEUR", "Comptabilité"),
        ("mmbaye", "pass123", "Mbaye", "Marie", "mmbaye@entreprise.com", "UTILISATEUR", "RH"),
        ("asy", "pass123", "Sy", "Awa", "asy@entreprise.com", "UTILISATEUR", "Marketing"),
        ("bfall", "pass123", "Fall", "Boubacar", "bfall@entreprise.com", "UTILISATEUR", "Comptabilité"),

        ("kdiop", "tech123", "Diop", "Khadim", "kdiop@entreprise.com", "TECHNICIEN", "Informatique"),
        ("ondiaye", "tech123", "Ndiaye", "Oumar", "ondiaye@entreprise.com", "TECHNICIEN", "Informatique"),
        ("fgueye", "tech123", "Gueye", "Fatou", "fgueye@entreprise.com", "TECHNICIEN", "Informatique"),

        ("asow", "admin123", "Sow", "Aminata", "asow@entreprise.com", "ADMIN", "Informatique"),
        ("mdiallo", "admin123", "Diallo", "Moussa", "mdiallo@entreprise.com", "ADMIN", "Direction"),
    ]

    ids = {}
    for login, password, nom, prenom, email, role, service in utilisateurs_data:
        try:
            utilisateur = Utilisateur(
                login=login, password=password, nom=nom, prenom=prenom,
                email=email, role=role, service=service
            )
            utilisateur.sauvegarder(db)
            ids[login] = utilisateur.id
            print(f" [{role}] {login} inséré (id={utilisateur.id})")
        except ValueError as e:
            print(f"  {login} ignoré : {e}")

    return ids


def inserer_incidents(db, ids_users):
    """Crée des incidents avec toutes les combinaisons priorité/statut"""
    incidents_data = [
        # titre, description, priorite, statut, signale_par (login)
        ("Imprimante en panne", "L'imprimante du 2e étage n'imprime plus rien depuis ce matin.", "BASSE", "OUVERT", "jdupont"),
        ("Écran qui clignote", "L'écran clignote par intermittence toutes les 30 secondes.", "BASSE", "RESOLU", "mmbaye"),

        ("Lenteur réseau", "Le réseau est très lent depuis hier après-midi.", "MOYENNE", "OUVERT", "asy"),
        ("Logiciel de paie bloqué", "Impossible d'ouvrir le logiciel de paie ce matin.", "MOYENNE", "EN_COURS", "mmbaye"),
        ("Souris défectueuse", "La souris ne répond plus correctement.", "MOYENNE", "FERME", "bfall"),

        ("Impossible de se connecter au VPN", "Le VPN refuse la connexion depuis hier soir.", "HAUTE", "OUVERT", "jdupont"),
        ("Boîte mail pleine", "Impossible de recevoir de nouveaux emails.", "HAUTE", "EN_COURS", "asy"),

        ("Écran bleu récurrent", "Le PC redémarre tout seul plusieurs fois par jour.", "CRITIQUE", "EN_COURS", "bfall"),
        ("Serveur de fichiers inaccessible", "Personne dans le service ne peut accéder aux fichiers partagés.", "CRITIQUE", "OUVERT", "mmbaye"),
    ]

    ids_incidents = []
    for titre, description, priorite, statut, login_signalant in incidents_data:
        try:
            incident = Incident(
                titre=titre,
                description=description,
                priorite=priorite,
                statut=statut,
                utilisateur_id=ids_users[login_signalant]
            )
            incident.sauvegarder(db)
            ids_incidents.append(incident.id)
            print(f" [{priorite}/{statut}] '{titre}' inséré (id={incident.id})")
        except ValueError as e:
            print(f"️  '{titre}' ignoré : {e}")

    return ids_incidents


def inserer_interventions(db, ids_incidents, ids_users):
    """Crée des interventions sur certains incidents (ceux en cours ou résolus/fermés)"""
    interventions_data = [
        # index_incident (0-based), commentaire, duree_minutes, technicien (login)
        (1, "Vérification des câbles et remplacement de l'écran.", 20, "kdiop"),
        (3, "Diagnostic du logiciel de paie, réinstallation en cours.", 40, "ondiaye"),
        (3, "Test après réinstallation, fonctionne à nouveau.", 15, "ondiaye"),
        (4, "Remplacement de la souris.", 5, "fgueye"),
        (6, "Vidage de la boîte mail et augmentation du quota.", 25, "kdiop"),
        (7, "Diagnostic initial effectué, en attente de pièce détachée.", 30, "fgueye"),
        (7, "Remplacement du composant défectueux et test.", 45, "fgueye"),
    ]

    for index_incident, commentaire, duree, login_technicien in interventions_data:
        try:
            intervention = Intervention(
                commentaire=commentaire,
                duree_minutes=duree,
                incident_id=ids_incidents[index_incident],
                technicien_id=ids_users[login_technicien]
            )
            intervention.sauvegarder(db)
            print(f" Intervention sur incident #{ids_incidents[index_incident]} insérée (id={intervention.id})")
        except ValueError as e:
            print(f"  Intervention ignorée : {e}")


def main():
    with Connexion() as db:
        if db.connection is None:
            print(" Connexion échouée")
            return

        print("\n--- Insertion des utilisateurs ---")
        ids_users = inserer_utilisateurs(db)

        print("\n--- Insertion des incidents ---")
        ids_incidents = inserer_incidents(db, ids_users)

        print("\n--- Insertion des interventions ---")
        inserer_interventions(db, ids_incidents, ids_users)

        print("\n Données de test insérées avec succès !")


if __name__ == "__main__":
    main()