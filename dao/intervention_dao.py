# dao/intervention_dao.py
from .base_dao import BaseDAO


class InterventionDAO(BaseDAO):
    """
    DAO pour la gestion des interventions
    """

    def __init__(self, connexion):
        super().__init__(connexion)
        self.table = 'intervention'
        self.primary_key = 'id'

    def ajouter(self, donnees):
        query = """
        INSERT INTO intervention (commentaire, duree_minutes, incident_id, technicien_id, date_intervention)
        VALUES (%s, %s, %s, %s, NOW())
        """
        params = (
            donnees.get('commentaire'),
            donnees.get('duree_minutes', 0),
            donnees.get('incident_id'),
            donnees.get('technicien_id')
        )
        return self.connexion.executer(query, params)

    def lister(self):
        query = """
        SELECT iv.*, 
               i.titre as incident_titre, i.priorite as incident_priorite,
               u.nom as technicien_nom, u.prenom as technicien_prenom,
               u2.nom as utilisateur_nom, u2.prenom as utilisateur_prenom
        FROM intervention iv
        LEFT JOIN incident i ON iv.incident_id = i.id
        LEFT JOIN utilisateur u ON iv.technicien_id = u.id
        LEFT JOIN utilisateur u2 ON i.utilisateur_id = u2.id
        ORDER BY iv.date_intervention DESC
        """
        return self.connexion.selectionner(query)

    def rechercher_par_id(self, id):
        query = """
        SELECT iv.*, 
               i.titre as incident_titre,
               u.nom as technicien_nom, u.prenom as technicien_prenom
        FROM intervention iv
        LEFT JOIN incident i ON iv.incident_id = i.id
        LEFT JOIN utilisateur u ON iv.technicien_id = u.id
        WHERE iv.id = %s
        """
        result = self.connexion.selectionner(query, (id,))
        return result[0] if result else None

    def rechercher(self, critere):
        query = """
        SELECT iv.*, 
               i.titre as incident_titre,
               u.nom as technicien_nom, u.prenom as technicien_prenom
        FROM intervention iv
        LEFT JOIN incident i ON iv.incident_id = i.id
        LEFT JOIN utilisateur u ON iv.technicien_id = u.id
        WHERE iv.commentaire LIKE %s
        ORDER BY iv.date_intervention DESC
        """
        critere_search = f"%{critere}%"
        return self.connexion.selectionner(query, (critere_search,))

    def modifier(self, id, donnees):
        set_parts = []
        params = []

        if 'commentaire' in donnees:
            set_parts.append("commentaire = %s")
            params.append(donnees['commentaire'])
        if 'duree_minutes' in donnees:
            set_parts.append("duree_minutes = %s")
            params.append(donnees['duree_minutes'])
        if 'incident_id' in donnees:
            set_parts.append("incident_id = %s")
            params.append(donnees['incident_id'])
        if 'technicien_id' in donnees:
            set_parts.append("technicien_id = %s")
            params.append(donnees['technicien_id'])

        if not set_parts:
            return False

        params.append(id)
        query = f"UPDATE intervention SET {', '.join(set_parts)} WHERE id = %s"
        return self.connexion.executer(query, tuple(params))

    def supprimer(self, id):
        query = "DELETE FROM intervention WHERE id = %s"
        return self.connexion.executer(query, (id,))

    def rechercher_par_incident(self, incident_id):
        query = """
        SELECT iv.*, u.nom, u.prenom, u.email 
        FROM intervention iv
        LEFT JOIN utilisateur u ON iv.technicien_id = u.id
        WHERE iv.incident_id = %s
        ORDER BY iv.date_intervention ASC
        """
        return self.connexion.selectionner(query, (incident_id,))

    def rechercher_par_technicien(self, technicien_id):
        query = """
        SELECT iv.*, 
               i.titre as incident_titre,
               u.nom as technicien_nom, u.prenom as technicien_prenom
        FROM intervention iv
        LEFT JOIN incident i ON iv.incident_id = i.id
        LEFT JOIN utilisateur u ON iv.technicien_id = u.id
        WHERE iv.technicien_id = %s
        ORDER BY iv.date_intervention DESC
        """
        return self.connexion.selectionner(query, (technicien_id,))

    def duree_totale_par_incident(self, incident_id):
        query = "SELECT SUM(duree_minutes) as total FROM intervention WHERE incident_id = %s"
        result = self.connexion.selectionner(query, (incident_id,))
        total = result[0]['total'] if result else 0
        return total if total is not None else 0

    def duree_totale_par_technicien(self, technicien_id):
        query = "SELECT SUM(duree_minutes) as total FROM intervention WHERE technicien_id = %s"
        result = self.connexion.selectionner(query, (technicien_id,))
        total = result[0]['total'] if result else 0
        return total if total is not None else 0
