# menu/interface.py
import sys
import os

# Ajouter le chemin du projet
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from database import Connexion
from models import Incident, Intervention, Utilisateur
from menu.auth import Auth


class Interface:
    """Interface utilisateur du système de gestion de tickets"""

    def __init__(self):
        self.db = Connexion()
        self.db.connecter()
        self.auth = Auth(self.db)

    def afficher_menu_principal(self):
        """Affiche le menu principal"""
        while True:
            print("\n" + "=" * 60)
            print(" " * 15 + "SYSTÈME DE GESTION DE TICKETS")
            print("=" * 60)

            if self.auth.est_connecte():
                u = self.auth.get_utilisateur_connecte()
                print(f"👤 Connecté : {u.prenom} {u.nom} ({u.role})")
            else:
                print("🔒 Non connecté")

            print("-" * 60)
            print("1. Gestion des utilisateurs")
            print("2. Gestion des incidents")
            print("3. Gestion des interventions")
            print("4. Voir mes tickets")
            print("5. Statistiques")
            print("6. Authentification")
            if self.auth.est_connecte():
                print("7. Mon compte")
                print("8. Quitter")
            else:
                print("7. Quitter")
            print("-" * 60)

            choix = input("Votre choix: ")

            if choix == "1":
                self.menu_utilisateurs()
            elif choix == "2":
                self.menu_incidents()
            elif choix == "3":
                self.menu_interventions()
            elif choix == "4":
                self.voir_mes_tickets()
            elif choix == "5":
                self.afficher_statistiques()
            elif choix == "6":
                self.menu_authentification()
            elif choix == "7":
                if self.auth.est_connecte():
                    self.menu_mon_compte()
                else:
                    print("\nAu revoir!")
                    self.db.fermer()
                    break
            elif choix == "8" and self.auth.est_connecte():
                print("\nAu revoir!")
                self.db.fermer()
                break
            else:
                print("\n❌ Choix invalide. Veuillez réessayer.")

    def menu_authentification(self):
        if self.auth.est_connecte():
            print("\n❌ Vous êtes déjà connecté.")
            return

        print("\n" + "-" * 50)
        print("AUTHENTIFICATION")
        print("-" * 50)
        print("1. Se connecter")
        print("2. Retour")
        print("-" * 50)

        choix = input("Votre choix: ")

        if choix == "1":
            self.auth.login()
        elif choix == "2":
            return
        else:
            print("\n❌ Choix invalide.")

    def menu_mon_compte(self):
        while True:
            print("\n" + "-" * 50)
            print("MON COMPTE")
            print("-" * 50)
            print("1. Voir mes informations")
            print("2. Changer mon mot de passe")
            print("3. Se déconnecter")
            print("4. Retour")
            print("-" * 50)

            choix = input("Votre choix: ")

            if choix == "1":
                self.auth.afficher_info_utilisateur()
            elif choix == "2":
                self.auth.changer_mot_de_passe()
            elif choix == "3":
                self.auth.logout()
                break
            elif choix == "4":
                break
            else:
                print("\n❌ Choix invalide.")

    # ============ GESTION DES UTILISATEURS ============

    def menu_utilisateurs(self):
        if not self.auth.est_connecte():
            print("\n❌ Vous devez être connecté pour accéder à cette fonctionnalité.")
            return

        if not self.auth.est_admin():
            print("\n❌ Vous devez être administrateur pour gérer les utilisateurs.")
            return

        while True:
            print("\n" + "-" * 50)
            print("GESTION DES UTILISATEURS")
            print("-" * 50)
            print("1. Ajouter un utilisateur")
            print("2. Lister les utilisateurs")
            print("3. Rechercher un utilisateur")
            print("4. Modifier un utilisateur")
            print("5. Supprimer un utilisateur")
            print("6. Retour")
            print("-" * 50)

            choix = input("Votre choix: ")

            if choix == "1":
                self.ajouter_utilisateur()
            elif choix == "2":
                self.lister_utilisateurs()
            elif choix == "3":
                self.rechercher_utilisateur()
            elif choix == "4":
                self.modifier_utilisateur()
            elif choix == "5":
                self.supprimer_utilisateur()
            elif choix == "6":
                break
            else:
                print("\n❌ Choix invalide.")

    def ajouter_utilisateur(self):
        print("\n" + "-" * 50)
        print("AJOUT D'UN UTILISATEUR")
        print("-" * 50)

        try:
            login = input("Login: ")
            password = input("Mot de passe: ")
            nom = input("Nom: ")
            prenom = input("Prénom: ")
            email = input("Email: ")

            print("\nRôles disponibles: UTILISATEUR, TECHNICIEN, ADMIN")
            role = input("Rôle: ").upper()

            service = input("Service (optionnel): ")

            utilisateur = Utilisateur(
                login=login,
                password=password,
                nom=nom,
                prenom=prenom,
                email=email,
                role=role,
                service=service if service else None
            )

            utilisateur.sauvegarder(self.db)
            print(f"\n✅ Utilisateur ajouté avec succès! (ID: {utilisateur.id})")
        except ValueError as e:
            print(f"\n❌ Erreur de validation: {e}")
        except Exception as e:
            print(f"\n❌ Erreur lors de l'ajout: {e}")

    def lister_utilisateurs(self):
        print("\n" + "-" * 50)
        print("LISTE DES UTILISATEURS")
        print("-" * 50)

        try:
            utilisateurs = Utilisateur.tous(self.db)
            if utilisateurs:
                print("\nID | Login | Nom | Prénom | Rôle | Service")
                print("-" * 65)
                for u in utilisateurs:
                    print(f"{u.id:2} | {u.login:10} | {u.nom:10} | {u.prenom:10} | {u.role:10} | {u.service or '-'}")
            else:
                print("\nAucun utilisateur trouvé.")
        except Exception as e:
            print(f"\n❌ Erreur lors du listage: {e}")

    def rechercher_utilisateur(self):
        print("\n" + "-" * 50)
        print("RECHERCHE D'UN UTILISATEUR")
        print("-" * 50)
        print("1. Par ID")
        print("2. Par Login")
        print("3. Par Rôle")
        print("-" * 50)

        choix = input("Votre choix: ")

        try:
            if choix == "1":
                id_util = input("ID: ")
                utilisateur = Utilisateur.trouver_par_id(self.db, id_util)
                if utilisateur:
                    self._afficher_utilisateur(utilisateur)
                else:
                    print("\n❌ Utilisateur non trouvé.")

            elif choix == "2":
                login = input("Login: ")
                utilisateur = Utilisateur.trouver_par_login(self.db, login)
                if utilisateur:
                    self._afficher_utilisateur(utilisateur)
                else:
                    print("\n❌ Utilisateur non trouvé.")

            elif choix == "3":
                role = input("Rôle (UTILISATEUR/TECHNICIEN/ADMIN): ").upper()
                utilisateurs = Utilisateur.trouver_par_role(self.db, role)
                if utilisateurs:
                    print(f"\n✅ {len(utilisateurs)} utilisateur(s) trouvé(s):")
                    for u in utilisateurs:
                        print(f"   - {u.prenom} {u.nom} ({u.login})")
                else:
                    print(f"\n❌ Aucun utilisateur avec le rôle {role}.")

            else:
                print("\n❌ Choix invalide.")
        except Exception as e:
            print(f"\n❌ Erreur lors de la recherche: {e}")

    def _afficher_utilisateur(self, utilisateur):
        print("\n" + "📋 DÉTAILS DE L'UTILISATEUR")
        print("-" * 40)
        print(f"ID: {utilisateur.id}")
        print(f"Login: {utilisateur.login}")
        print(f"Nom: {utilisateur.nom}")
        print(f"Prénom: {utilisateur.prenom}")
        print(f"Email: {utilisateur.email}")
        print(f"Rôle: {utilisateur.role}")
        print(f"Service: {utilisateur.service or '-'}")
        print(f"Date création: {utilisateur.date_creation}")

    def modifier_utilisateur(self):
        print("\n" + "-" * 50)
        print("MODIFICATION D'UN UTILISATEUR")
        print("-" * 50)

        try:
            id_util = input("ID de l'utilisateur à modifier: ")
            utilisateur = Utilisateur.trouver_par_id(self.db, id_util)
            if not utilisateur:
                print("\n❌ Utilisateur non trouvé.")
                return

            print(f"\nModification de: {utilisateur.prenom} {utilisateur.nom}")
            print("(Laissez vide pour conserver la valeur actuelle)")

            login = input(f"Login ({utilisateur.login}): ") or utilisateur.login
            nom = input(f"Nom ({utilisateur.nom}): ") or utilisateur.nom
            prenom = input(f"Prénom ({utilisateur.prenom}): ") or utilisateur.prenom
            email = input(f"Email ({utilisateur.email}): ") or utilisateur.email
            role = input(f"Rôle ({utilisateur.role}): ").upper() or utilisateur.role
            service = input(f"Service ({utilisateur.service or '-'}): ") or utilisateur.service

            utilisateur.login = login
            utilisateur.nom = nom
            utilisateur.prenom = prenom
            utilisateur.email = email
            utilisateur.role = role
            utilisateur.service = service

            changer_mdp = input("\nVoulez-vous changer le mot de passe? (o/n): ")
            if changer_mdp.lower() == 'o':
                nouveau_mdp = input("Nouveau mot de passe: ")
                utilisateur.password = nouveau_mdp

            utilisateur.sauvegarder(self.db)
            print("\n✅ Utilisateur modifié avec succès!")
        except ValueError as e:
            print(f"\n❌ Erreur de validation: {e}")
        except Exception as e:
            print(f"\n❌ Erreur lors de la modification: {e}")

    def supprimer_utilisateur(self):
        print("\n" + "-" * 50)
        print("SUPPRESSION D'UN UTILISATEUR")
        print("-" * 50)

        try:
            id_util = input("ID de l'utilisateur à supprimer: ")
            utilisateur = Utilisateur.trouver_par_id(self.db, id_util)
            if not utilisateur:
                print("\n❌ Utilisateur non trouvé.")
                return

            if utilisateur.id == self.auth.get_utilisateur_connecte().id:
                print("\n❌ Vous ne pouvez pas supprimer votre propre compte.")
                return

            print(f"\n⚠️  Vous allez supprimer: {utilisateur.prenom} {utilisateur.nom}")
            confirmation = input("Confirmer la suppression? (o/n): ")

            if confirmation.lower() == 'o':
                utilisateur.supprimer(self.db)
                print("\n✅ Utilisateur supprimé avec succès!")
            else:
                print("\nSuppression annulée.")
        except Exception as e:
            print(f"\n❌ Erreur lors de la suppression: {e}")

    # ============ GESTION DES INCIDENTS ============

    def menu_incidents(self):
        if not self.auth.est_connecte():
            print("\n❌ Vous devez être connecté pour accéder à cette fonctionnalité.")
            return

        while True:
            print("\n" + "-" * 50)
            print("GESTION DES INCIDENTS")
            print("-" * 50)
            print("1. Créer un incident")
            print("2. Lister les incidents")
            print("3. Rechercher un incident")
            print("4. Modifier un incident")
            print("5. Supprimer un incident")
            print("6. Changer le statut d'un incident")
            print("7. Retour")
            print("-" * 50)

            choix = input("Votre choix: ")

            if choix == "1":
                self.creer_incident()
            elif choix == "2":
                self.lister_incidents()
            elif choix == "3":
                self.rechercher_incident()
            elif choix == "4":
                self.modifier_incident()
            elif choix == "5":
                self.supprimer_incident()
            elif choix == "6":
                self.changer_statut_incident()
            elif choix == "7":
                break
            else:
                print("\n❌ Choix invalide.")

    def creer_incident(self):
        if not self.auth.est_connecte():
            print("\n❌ Vous devez être connecté pour créer un incident.")
            return

        print("\n" + "-" * 50)
        print("CRÉATION D'UN INCIDENT")
        print("-" * 50)

        try:
            titre = input("Titre: ")
            description = input("Description: ")
            priorite = input("Priorité (BASSE/MOYENNE/HAUTE/CRITIQUE): ").upper()

            incident = Incident(
                titre=titre,
                description=description,
                priorite=priorite,
                utilisateur_id=self.auth.get_utilisateur_connecte().id
            )

            incident.sauvegarder(self.db)
            print(f"\n✅ Incident créé avec succès! (ID: {incident.id})")
        except ValueError as e:
            print(f"\n❌ Erreur de validation: {e}")
        except Exception as e:
            print(f"\n❌ Erreur lors de la création: {e}")

    def lister_incidents(self):
        print("\n" + "-" * 50)
        print("LISTE DES INCIDENTS")
        print("-" * 50)

        try:
            incidents = Incident.tous(self.db)
            if incidents:
                print("\nID | Titre | Priorité | Statut | Date")
                print("-" * 60)
                for inc in incidents:
                    print(f"{inc.id:2} | {inc.titre[:30]:30} | {inc.priorite:8} | {inc.statut:8} | {inc.date_creation.strftime('%Y-%m-%d %H:%M')}")
            else:
                print("\nAucun incident trouvé.")
        except Exception as e:
            print(f"\n❌ Erreur lors du listage: {e}")

    def rechercher_incident(self):
        print("\n" + "-" * 50)
        print("RECHERCHE D'UN INCIDENT")
        print("-" * 50)
        print("1. Par ID")
        print("2. Par Statut")
        print("3. Par Priorité")
        print("4. Par Utilisateur")
        print("-" * 50)

        choix = input("Votre choix: ")

        try:
            if choix == "1":
                id_inc = input("ID: ")
                incident = Incident.trouver_par_id(self.db, id_inc)
                if incident:
                    self._afficher_incident(incident)
                else:
                    print("\n❌ Incident non trouvé.")

            elif choix == "2":
                statut = input("Statut (OUVERT/EN_COURS/RESOLU/FERME): ").upper()
                incidents = Incident.trouver_par_statut(self.db, statut)
                if incidents:
                    print(f"\n✅ {len(incidents)} incident(s) trouvé(s):")
                    for inc in incidents:
                        print(f"   - #{inc.id}: {inc.titre} ({inc.priorite})")
                else:
                    print(f"\n❌ Aucun incident avec le statut {statut}.")

            elif choix == "3":
                priorite = input("Priorité (BASSE/MOYENNE/HAUTE/CRITIQUE): ").upper()
                incidents = Incident.trouver_par_priorite(self.db, priorite)
                if incidents:
                    print(f"\n✅ {len(incidents)} incident(s) trouvé(s):")
                    for inc in incidents:
                        print(f"   - #{inc.id}: {inc.titre} ({inc.statut})")
                else:
                    print(f"\n❌ Aucun incident avec la priorité {priorite}.")

            elif choix == "4":
                id_util = input("ID de l'utilisateur: ")
                incidents = Incident.trouver_par_utilisateur(self.db, id_util)
                if incidents:
                    print(f"\n✅ {len(incidents)} incident(s) trouvé(s):")
                    for inc in incidents:
                        print(f"   - #{inc.id}: {inc.titre} ({inc.statut})")
                else:
                    print(f"\n❌ Aucun incident pour cet utilisateur.")

            else:
                print("\n❌ Choix invalide.")
        except Exception as e:
            print(f"\n❌ Erreur lors de la recherche: {e}")

    def _afficher_incident(self, incident):
        print("\n" + "📋 DÉTAILS DE L'INCIDENT")
        print("-" * 40)
        print(f"ID: {incident.id}")
        print(f"Titre: {incident.titre}")
        print(f"Description: {incident.description}")
        print(f"Priorité: {incident.priorite}")
        print(f"Statut: {incident.statut}")
        print(f"Date création: {incident.date_creation}")

        utilisateur = incident.get_utilisateur(self.db)
        if utilisateur:
            print(f"Créé par: {utilisateur.prenom} {utilisateur.nom}")

        interventions = incident.get_interventions(self.db)
        if interventions:
            print(f"\n📝 Interventions associées ({len(interventions)}):")
            for inter in interventions:
                print(f"   - #{inter.id}: {inter.commentaire[:40]}... ({inter.duree_minutes} min)")
        else:
            print("\n📝 Aucune intervention associée.")

    def modifier_incident(self):
        print("\n" + "-" * 50)
        print("MODIFICATION D'UN INCIDENT")
        print("-" * 50)

        try:
            id_inc = input("ID de l'incident à modifier: ")
            incident = Incident.trouver_par_id(self.db, id_inc)
            if not incident:
                print("\n❌ Incident non trouvé.")
                return

            if not self.auth.est_admin() and incident.utilisateur_id != self.auth.get_utilisateur_connecte().id:
                print("\n❌ Vous ne pouvez modifier que vos propres incidents.")
                return

            print(f"\nModification de: {incident.titre}")
            print("(Laissez vide pour conserver la valeur actuelle)")

            titre = input(f"Titre ({incident.titre}): ") or incident.titre
            description = input(f"Description ({incident.description[:30]}...): ") or incident.description
            priorite = input(f"Priorité ({incident.priorite}): ").upper() or incident.priorite
            statut = input(f"Statut ({incident.statut}): ").upper() or incident.statut

            incident.titre = titre
            incident.description = description
            incident.priorite = priorite
            incident.statut = statut

            incident.sauvegarder(self.db)
            print("\n✅ Incident modifié avec succès!")
        except ValueError as e:
            print(f"\n❌ Erreur de validation: {e}")
        except Exception as e:
            print(f"\n❌ Erreur lors de la modification: {e}")

    def supprimer_incident(self):
        print("\n" + "-" * 50)
        print("SUPPRESSION D'UN INCIDENT")
        print("-" * 50)

        try:
            id_inc = input("ID de l'incident à supprimer: ")
            incident = Incident.trouver_par_id(self.db, id_inc)
            if not incident:
                print("\n❌ Incident non trouvé.")
                return

            if not self.auth.est_admin() and incident.utilisateur_id != self.auth.get_utilisateur_connecte().id:
                print("\n❌ Vous ne pouvez supprimer que vos propres incidents.")
                return

            print(f"\n⚠️  Vous allez supprimer: {incident.titre}")
            confirmation = input("Confirmer la suppression? (o/n): ")

            if confirmation.lower() == 'o':
                incident.supprimer(self.db)
                print("\n✅ Incident supprimé avec succès!")
            else:
                print("\nSuppression annulée.")
        except Exception as e:
            print(f"\n❌ Erreur lors de la suppression: {e}")

    def changer_statut_incident(self):
        print("\n" + "-" * 50)
        print("CHANGEMENT DE STATUT D'UN INCIDENT")
        print("-" * 50)

        try:
            id_inc = input("ID de l'incident: ")
            incident = Incident.trouver_par_id(self.db, id_inc)
            if not incident:
                print("\n❌ Incident non trouvé.")
                return

            print(f"\nIncident: {incident.titre}")
            print(f"Statut actuel: {incident.statut}")
            print("\nStatuts disponibles: OUVERT, EN_COURS, RESOLU, FERME")

            nouveau_statut = input("Nouveau statut: ").upper()
            incident.changer_statut(self.db, nouveau_statut)
            print(f"\n✅ Statut changé en {nouveau_statut} avec succès!")
        except ValueError as e:
            print(f"\n❌ Erreur: {e}")
        except Exception as e:
            print(f"\n❌ Erreur lors du changement de statut: {e}")

    # ============ GESTION DES INTERVENTIONS ============

    def menu_interventions(self):
        if not self.auth.est_connecte():
            print("\n❌ Vous devez être connecté pour accéder à cette fonctionnalité.")
            return

        while True:
            print("\n" + "-" * 50)
            print("GESTION DES INTERVENTIONS")
            print("-" * 50)
            print("1. Ajouter une intervention")
            print("2. Lister les interventions")
            print("3. Rechercher une intervention")
            print("4. Modifier une intervention")
            print("5. Supprimer une intervention")
            print("6. Voir les interventions d'un incident")
            print("7. Retour")
            print("-" * 50)

            choix = input("Votre choix: ")

            if choix == "1":
                self.ajouter_intervention()
            elif choix == "2":
                self.lister_interventions()
            elif choix == "3":
                self.rechercher_intervention()
            elif choix == "4":
                self.modifier_intervention()
            elif choix == "5":
                self.supprimer_intervention()
            elif choix == "6":
                self.voir_interventions_incident()
            elif choix == "7":
                break
            else:
                print("\n❌ Choix invalide.")

    def ajouter_intervention(self):
        if not self.auth.est_connecte():
            print("\n❌ Vous devez être connecté pour ajouter une intervention.")
            return

        print("\n" + "-" * 50)
        print("AJOUT D'UNE INTERVENTION")
        print("-" * 50)

        try:
            incident_id = input("ID de l'incident: ")

            incident = Incident.trouver_par_id(self.db, incident_id)
            if not incident:
                print("\n❌ Incident non trouvé.")
                return

            commentaire = input("Commentaire: ")
            duree_minutes = int(input("Durée (en minutes): "))

            intervention = Intervention(
                commentaire=commentaire,
                duree_minutes=duree_minutes,
                incident_id=incident_id,
                technicien_id=self.auth.get_utilisateur_connecte().id
            )

            intervention.sauvegarder(self.db)
            print(f"\n✅ Intervention ajoutée avec succès! (ID: {intervention.id})")
        except ValueError as e:
            print(f"\n❌ Erreur de validation: {e}")
        except Exception as e:
            print(f"\n❌ Erreur lors de l'ajout: {e}")

    def lister_interventions(self):
        print("\n" + "-" * 50)
        print("LISTE DES INTERVENTIONS")
        print("-" * 50)

        try:
            interventions = Intervention.tous(self.db)
            if interventions:
                print("\nID | Incident | Technicien | Durée | Commentaire")
                print("-" * 70)
                for inter in interventions:
                    incident = inter.get_incident(self.db)
                    technicien = inter.get_technicien(self.db)
                    incident_titre = incident.titre if incident else "N/A"
                    technicien_nom = f"{technicien.prenom} {technicien.nom}" if technicien else "N/A"
                    print(f"{inter.id:2} | {incident_titre[:20]:20} | {technicien_nom:20} | {inter.duree_minutes:4} min | {inter.commentaire[:20]}...")
            else:
                print("\nAucune intervention trouvée.")
        except Exception as e:
            print(f"\n❌ Erreur lors du listage: {e}")

    def rechercher_intervention(self):
        print("\n" + "-" * 50)
        print("RECHERCHE D'UNE INTERVENTION")
        print("-" * 50)
        print("1. Par ID")
        print("2. Par Incident")
        print("3. Par Technicien")
        print("-" * 50)

        choix = input("Votre choix: ")

        try:
            if choix == "1":
                id_inter = input("ID: ")
                intervention = Intervention.trouver_par_id(self.db, id_inter)
                if intervention:
                    self._afficher_intervention(intervention)
                else:
                    print("\n❌ Intervention non trouvée.")

            elif choix == "2":
                incident_id = input("ID de l'incident: ")
                interventions = Intervention.trouver_par_incident(self.db, incident_id)
                if interventions:
                    print(f"\n✅ {len(interventions)} intervention(s) trouvée(s):")
                    for inter in interventions:
                        print(f"   - #{inter.id}: {inter.commentaire[:40]}... ({inter.duree_minutes} min)")
                else:
                    print(f"\n❌ Aucune intervention pour cet incident.")

            elif choix == "3":
                technicien_id = input("ID du technicien: ")
                interventions = Intervention.trouver_par_technicien(self.db, technicien_id)
                if interventions:
                    print(f"\n✅ {len(interventions)} intervention(s) trouvée(s):")
                    for inter in interventions:
                        print(f"   - #{inter.id}: {inter.commentaire[:40]}... ({inter.duree_minutes} min)")
                else:
                    print(f"\n❌ Aucune intervention pour ce technicien.")

            else:
                print("\n❌ Choix invalide.")
        except Exception as e:
            print(f"\n❌ Erreur lors de la recherche: {e}")

    def _afficher_intervention(self, intervention):
        print("\n" + "📋 DÉTAILS DE L'INTERVENTION")
        print("-" * 40)
        print(f"ID: {intervention.id}")
        print(f"Commentaire: {intervention.commentaire}")
        print(f"Durée: {intervention.duree_minutes} minutes")
        print(f"Date: {intervention.date_intervention}")

        incident = intervention.get_incident(self.db)
        if incident:
            print(f"Incident: #{incident.id} - {incident.titre}")

        technicien = intervention.get_technicien(self.db)
        if technicien:
            print(f"Technicien: {technicien.prenom} {technicien.nom}")

    def modifier_intervention(self):
        print("\n" + "-" * 50)
        print("MODIFICATION D'UNE INTERVENTION")
        print("-" * 50)

        try:
            id_inter = input("ID de l'intervention à modifier: ")
            intervention = Intervention.trouver_par_id(self.db, id_inter)
            if not intervention:
                print("\n❌ Intervention non trouvée.")
                return

            if not self.auth.est_admin() and intervention.technicien_id != self.auth.get_utilisateur_connecte().id:
                print("\n❌ Vous ne pouvez modifier que vos propres interventions.")
                return

            print(f"\nModification de l'intervention #{intervention.id}")
            print("(Laissez vide pour conserver la valeur actuelle)")

            commentaire = input(f"Commentaire ({intervention.commentaire[:30]}...): ") or intervention.commentaire
            duree_str = input(f"Durée ({intervention.duree_minutes} min): ")
            duree_minutes = int(duree_str) if duree_str else intervention.duree_minutes

            intervention.commentaire = commentaire
            intervention.duree_minutes = duree_minutes

            intervention.sauvegarder(self.db)
            print("\n✅ Intervention modifiée avec succès!")
        except ValueError as e:
            print(f"\n❌ Erreur de validation: {e}")
        except Exception as e:
            print(f"\n❌ Erreur lors de la modification: {e}")

    def supprimer_intervention(self):
        print("\n" + "-" * 50)
        print("SUPPRESSION D'UNE INTERVENTION")
        print("-" * 50)

        try:
            id_inter = input("ID de l'intervention à supprimer: ")
            intervention = Intervention.trouver_par_id(self.db, id_inter)
            if not intervention:
                print("\n❌ Intervention non trouvée.")
                return

            if not self.auth.est_admin() and intervention.technicien_id != self.auth.get_utilisateur_connecte().id:
                print("\n❌ Vous ne pouvez supprimer que vos propres interventions.")
                return

            print(f"\n⚠️  Vous allez supprimer l'intervention #{intervention.id}")
            confirmation = input("Confirmer la suppression? (o/n): ")

            if confirmation.lower() == 'o':
                intervention.supprimer(self.db)
                print("\n✅ Intervention supprimée avec succès!")
            else:
                print("\nSuppression annulée.")
        except Exception as e:
            print(f"\n❌ Erreur lors de la suppression: {e}")

    def voir_interventions_incident(self):
        print("\n" + "-" * 50)
        print("INTERVENTIONS D'UN INCIDENT")
        print("-" * 50)

        incident_id = input("ID de l'incident: ")

        try:
            incident = Incident.trouver_par_id(self.db, incident_id)
            if not incident:
                print("\n❌ Incident non trouvé.")
                return

            interventions = incident.get_interventions(self.db)
            if interventions:
                print(f"\n📝 Interventions pour l'incident #{incident_id}: {incident.titre}")
                print("-" * 50)
                for inter in interventions:
                    technicien = inter.get_technicien(self.db)
                    nom_tech = f"{technicien.prenom} {technicien.nom}" if technicien else "N/A"
                    print(f"#{inter.id} - {nom_tech}: {inter.commentaire[:40]}... ({inter.duree_minutes} min)")
            else:
                print(f"\nAucune intervention pour l'incident #{incident_id}")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")

    def voir_mes_tickets(self):
        if not self.auth.est_connecte():
            print("\n❌ Vous devez être connecté pour voir vos tickets.")
            return

        u = self.auth.get_utilisateur_connecte()
        print(f"\n" + "-" * 50)
        print(f"MES TICKETS - {u.prenom} {u.nom}")
        print("-" * 50)

        try:
            incidents = Incident.trouver_par_utilisateur(self.db, u.id)
            if incidents:
                print(f"\n📊 {len(incidents)} incident(s) trouvé(s):")
                print("\nID | Titre | Priorité | Statut | Date")
                print("-" * 60)
                for inc in incidents:
                    print(f"{inc.id:2} | {inc.titre[:30]:30} | {inc.priorite:8} | {inc.statut:8} | {inc.date_creation.strftime('%Y-%m-%d %H:%M')}")

                    interventions = inc.get_interventions(self.db)
                    if interventions:
                        print(f"    📝 {len(interventions)} intervention(s):")
                        for inter in interventions:
                            print(f"       - #{inter.id}: {inter.commentaire[:30]}... ({inter.duree_minutes} min)")
            else:
                print("\nVous n'avez aucun ticket.")
        except Exception as e:
            print(f"\n❌ Erreur lors de l'affichage: {e}")

    def afficher_statistiques(self):
        print("\n" + "-" * 50)
        print("STATISTIQUES")
        print("-" * 50)

        try:
            incidents = Incident.tous(self.db)
            nb_incidents = len(incidents)

            stats_statuts = Incident.compter_par_statut(self.db)

            interventions = Intervention.tous(self.db)
            nb_interventions = len(interventions)

            utilisateurs = Utilisateur.tous(self.db)
            nb_utilisateurs = len(utilisateurs)

            temps_total = sum(inter.duree_minutes for inter in interventions)

            print(f"\n📊 Nombre total d'incidents: {nb_incidents}")
            print(f"📊 Nombre total d'interventions: {nb_interventions}")
            print(f"📊 Nombre total d'utilisateurs: {nb_utilisateurs}")
            print(f"📊 Temps total passé: {temps_total} minutes")

            print("\n📊 Répartition des incidents par statut:")
            for statut, nb in stats_statuts.items():
                print(f"   - {statut}: {nb}")

            if self.auth.est_connecte():
                temps_utilisateur = Intervention.duree_totale_par_technicien(
                    self.db, self.auth.get_utilisateur_connecte().id
                )
                print(f"\n⏱️  Votre temps total d'intervention: {temps_utilisateur} minutes")

        except Exception as e:
            print(f"\n❌ Erreur lors du calcul des statistiques: {e}")