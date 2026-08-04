# dao/incident_dao.py
from .base_dao import BaseDAO


class IncidentDAO(BaseDAO):
    """
    DAO pour la gestion des incidents
    """

    def __init__(self, connexion):
        super().__init__(connexion)
        self.table = 'incident'
        self.primary_key = 'id'

    def ajouter(self, donnees):
        query = """
        INSERT INTO incident (titre, description, priorite, statut, utilisateur_id, date_creation)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        params = (
            donnees.get('titre'),
            donnees.get('description'),
            donnees.get('priorite', 'MOYENNE'),
            donnees.get('statut', 'OUVERT'),
            donnees.get('utilisateur_id')
        )
        return self.connexion.executer(query, params)

    def lister(self):
        query = """
        SELECT i.*, u.nom, u.prenom, u.email 
        FROM incident i
        LEFT JOIN utilisateur u ON i.utilisateur_id = u.id
        ORDER BY i.date_creation DESC
        """
        return self.connexion.selectionner(query)

    def rechercher_par_id(self, id):
        query = """
        SELECT i.*, u.nom, u.prenom, u.email 
        FROM incident i
        LEFT JOIN utilisateur u ON i.utilisateur_id = u.id
        WHERE i.id = %s
        """
        result = self.connexion.selectionner(query, (id,))
        return result[0] if result else None

    def rechercher(self, critere):
        query = """
        SELECT i.*, u.nom, u.prenom, u.email 
        FROM incident i
        LEFT JOIN utilisateur u ON i.utilisateur_id = u.id
        WHERE i.titre LIKE %s OR i.description LIKE %s
        ORDER BY i.date_creation DESC
        """
        critere_search = f"%{critere}%"
        return self.connexion.selectionner(query, (critere_search, critere_search))

    def modifier(self, id, donnees):
        set_parts = []
        params = []

        if 'titre' in donnees:
            set_parts.append("titre = %s")
            params.append(donnees['titre'])
        if 'description' in donnees:
            set_parts.append("description = %s")
            params.append(donnees['description'])
        if 'priorite' in donnees:
            set_parts.append("priorite = %s")
            params.append(donnees['priorite'])
        if 'statut' in donnees:
            set_parts.append("statut = %s")
            params.append(donnees['statut'])
        if 'utilisateur_id' in donnees:
            set_parts.append("utilisateur_id = %s")
            params.append(donnees['utilisateur_id'])

        if not set_parts:
            return False

        params.append(id)
        query = f"UPDATE incident SET {', '.join(set_parts)} WHERE id = %s"
        return self.connexion.executer(query, tuple(params))

    def supprimer(self, id):
        query = "DELETE FROM incident WHERE id = %s"
        return self.connexion.executer(query, (id,))

    def rechercher_par_utilisateur(self, utilisateur_id):
        query = """
        SELECT i.*, u.nom, u.prenom, u.email 
        FROM incident i
        LEFT JOIN utilisateur u ON i.utilisateur_id = u.id
        WHERE i.utilisateur_id = %s
        ORDER BY i.date_creation DESC
        """
        return self.connexion.selectionner(query, (utilisateur_id,))

    def rechercher_par_statut(self, statut):
        query = """
        SELECT i.*, u.nom, u.prenom, u.email 
        FROM incident i
        LEFT JOIN utilisateur u ON i.utilisateur_id = u.id
        WHERE i.statut = %s
        ORDER BY i.date_creation DESC
        """
        return self.connexion.selectionner(query, (statut,))

    def rechercher_par_priorite(self, priorite):
        query = """
        SELECT i.*, u.nom, u.prenom, u.email 
        FROM incident i
        LEFT JOIN utilisateur u ON i.utilisateur_id = u.id
        WHERE i.priorite = %s
        ORDER BY i.date_creation DESC
        """
        return self.connexion.selectionner(query, (priorite,))

    def compter_par_statut(self):
        query = "SELECT statut, COUNT(*) as total FROM incident GROUP BY statut"
        results = self.connexion.selectionner(query)
        return {result['statut']: result['total'] for result in results}

    def changer_statut(self, id, nouveau_statut):
        query = "UPDATE incident SET statut = %s WHERE id = %s"
        return self.connexion.executer(query, (nouveau_statut, id))

    def get_interventions(self, incident_id):
        query = """
        SELECT iv.*, u.nom, u.prenom, u.email 
        FROM intervention iv
        LEFT JOIN utilisateur u ON iv.technicien_id = u.id
        WHERE iv.incident_id = %s
        ORDER BY iv.date_intervention DESC
        """
        return self.connexion.selectionner(query, (incident_id,))