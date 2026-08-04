# dao/base_dao.py
from abc import ABC, abstractmethod


class BaseDAO(ABC):
    """
    Classe de base abstraite pour tous les DAO
    """

    def __init__(self, connexion):
        self.connexion = connexion
        self.table = None
        self.primary_key = 'id'

    @abstractmethod
    def ajouter(self, donnees):
        pass

    @abstractmethod
    def lister(self):
        pass

    @abstractmethod
    def rechercher_par_id(self, id):
        pass

    @abstractmethod
    def modifier(self, id, donnees):
        pass

    @abstractmethod
    def supprimer(self, id):
        pass

    def compter(self):
        if not self.table:
            return 0
        query = f"SELECT COUNT(*) as total FROM {self.table}"
        result = self.connexion.selectionner(query)
        return result[0]['total'] if result else 0

    def existe(self, id):
        if not self.table:
            return False
        query = f"SELECT COUNT(*) as total FROM {self.table} WHERE {self.primary_key} = %s"
        result = self.connexion.selectionner(query, (id,))
        return result[0]['total'] > 0 if result else False