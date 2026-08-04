# dao/utilisateur_dao.py
import hashlib
from .base_dao import BaseDAO


class UtilisateurDAO(BaseDAO):
    """
    DAO pour la gestion des utilisateurs
    """

    def __init__(self, connexion):
        super().__init__(connexion)
        self.table = 'utilisateur'
        self.primary_key = 'id'

    def _hasher_mot_de_passe(self, mot_de_passe):
        return hashlib.sha256(mot_de_passe.encode()).hexdigest()

    def ajouter(self, donnees):
        query = """
        INSERT INTO utilisateur (login, password, nom, prenom, email, role, service, date_creation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        mot_de_passe_hash = self._hasher_mot_de_passe(donnees.get('password'))
        params = (
            donnees.get('login'),
            mot_de_passe_hash,
            donnees.get('nom'),
            donnees.get('prenom'),
            donnees.get('email'),
            donnees.get('role', 'UTILISATEUR'),
            donnees.get('service')
        )
        return self.connexion.executer(query, params)

    def lister(self):
        query = """
        SELECT id, login, nom, prenom, email, role, service, date_creation
        FROM utilisateur
        ORDER BY nom, prenom
        """
        return self.connexion.selectionner(query)

    def rechercher_par_id(self, id):
        query = """
        SELECT id, login, nom, prenom, email, role, service, date_creation
        FROM utilisateur
        WHERE id = %s
        """
        result = self.connexion.selectionner(query, (id,))
        return result[0] if result else None

    def rechercher(self, critere):
        query = """
        SELECT id, login, nom, prenom, email, role, service, date_creation
        FROM utilisateur
        WHERE nom LIKE %s OR prenom LIKE %s OR email LIKE %s
        ORDER BY nom, prenom
        """
        critere_search = f"%{critere}%"
        return self.connexion.selectionner(query, (critere_search, critere_search, critere_search))

    def modifier(self, id, donnees):
        set_parts = []
        params = []

        if 'login' in donnees:
            set_parts.append("login = %s")
            params.append(donnees['login'])
        if 'password' in donnees and donnees['password']:
            set_parts.append("password = %s")
            params.append(self._hasher_mot_de_passe(donnees['password']))
        if 'nom' in donnees:
            set_parts.append("nom = %s")
            params.append(donnees['nom'])
        if 'prenom' in donnees:
            set_parts.append("prenom = %s")
            params.append(donnees['prenom'])
        if 'email' in donnees:
            set_parts.append("email = %s")
            params.append(donnees['email'])
        if 'role' in donnees:
            set_parts.append("role = %s")
            params.append(donnees['role'])
        if 'service' in donnees:
            set_parts.append("service = %s")
            params.append(donnees['service'])

        if not set_parts:
            return False

        params.append(id)
        query = f"UPDATE utilisateur SET {', '.join(set_parts)} WHERE id = %s"
        return self.connexion.executer(query, tuple(params))

    def supprimer(self, id):
        query = "DELETE FROM utilisateur WHERE id = %s"
        return self.connexion.executer(query, (id,))

    def rechercher_par_login(self, login):
        query = """
        SELECT id, login, password, nom, prenom, email, role, service, date_creation
        FROM utilisateur
        WHERE login = %s
        """
        result = self.connexion.selectionner(query, (login,))
        return result[0] if result else None

    def rechercher_par_role(self, role):
        query = """
        SELECT id, login, nom, prenom, email, role, service, date_creation
        FROM utilisateur
        WHERE role = %s
        ORDER BY nom, prenom
        """
        return self.connexion.selectionner(query, (role,))

    def authentifier(self, login, password):
        password_hash = self._hasher_mot_de_passe(password)
        query = """
        SELECT id, login, nom, prenom, email, role, service, date_creation
        FROM utilisateur
        WHERE login = %s AND password = %s
        """
        result = self.connexion.selectionner(query, (login, password_hash))
        return result[0] if result else None