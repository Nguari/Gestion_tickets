from datetime import datetime


class Incident:
    PRIORITES_VALIDES = ("BASSE", "MOYENNE", "HAUTE", "CRITIQUE")
    STATUTS_VALIDES = ("OUVERT", "EN_COURS", "RESOLU", "FERME")

    def __init__(self, titre, description, utilisateur_id,
                 priorite="MOYENNE", statut="OUVERT",
                 id=None, date_creation=None):
        self.id = id
        self.titre = titre
        self.description = description
        self.priorite = priorite
        self.statut = statut
        self.utilisateur_id = utilisateur_id
        self.date_creation = date_creation or datetime.now()

        self._valider()

    # --- Validation ---
    def _valider(self):
        if not self.titre or not self.titre.strip():
            raise ValueError("Le titre est obligatoire")

        if not self.description or not self.description.strip():
            raise ValueError("La description est obligatoire")

        if self.utilisateur_id is None:
            raise ValueError("L'utilisateur_id est obligatoire")

        if self.priorite not in self.PRIORITES_VALIDES:
            raise ValueError(f"Priorité invalide : {self.priorite}. Doit être parmi {self.PRIORITES_VALIDES}")

        if self.statut not in self.STATUTS_VALIDES:
            raise ValueError(f"Statut invalide : {self.statut}. Doit être parmi {self.STATUTS_VALIDES}")

    # --- Représentation ---
    def __repr__(self):
        return (f"Incident(id={self.id}, titre='{self.titre}', "
                f"priorite='{self.priorite}', statut='{self.statut}')")

    def __str__(self):
        return f"#{self.id} [{self.priorite}/{self.statut}] {self.titre}"

    # --- Sauvegarde (insertion ou mise à jour) ---
    def sauvegarder(self, db):
        if self.id is None:
            self.id = db.executer(
                """INSERT INTO incident (titre, description, priorite, statut, date_creation, utilisateur_id)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (self.titre, self.description, self.priorite, self.statut,
                 self.date_creation, self.utilisateur_id)
            )
        else:
            db.executer(
                """UPDATE incident
                   SET titre=%s, description=%s, priorite=%s, statut=%s, utilisateur_id=%s
                   WHERE id=%s""",
                (self.titre, self.description, self.priorite, self.statut,
                 self.utilisateur_id, self.id)
            )
        return self.id

    def supprimer(self, db):
        if self.id is None:
            raise ValueError("Impossible de supprimer un incident sans id")
        db.executer("DELETE FROM incident WHERE id=%s", (self.id,))

    # --- Changement de statut (méthode métier pratique) ---
    def changer_statut(self, db, nouveau_statut):
        if nouveau_statut not in self.STATUTS_VALIDES:
            raise ValueError(f"Statut invalide : {nouveau_statut}")
        self.statut = nouveau_statut
        db.executer("UPDATE incident SET statut=%s WHERE id=%s", (nouveau_statut, self.id))

    # --- Relations (récupérer les objets liés) ---
    def get_utilisateur(self, db):
        """L'utilisateur qui a signalé l'incident"""
        from .Utilisateur import Utilisateur
        return Utilisateur.trouver_par_id(db, self.utilisateur_id)

    def get_interventions(self, db):
        """Toutes les interventions liées à cet incident"""
        from .Intervention import Intervention
        return Intervention.trouver_par_incident(db, self.id)

    # --- Méthodes de classe pour la lecture ---
    @classmethod
    def _depuis_ligne(cls, ligne):
        id, titre, description, priorite, statut, date_creation, utilisateur_id = ligne
        return cls(
            titre=titre,
            description=description,
            priorite=priorite,
            statut=statut,
            utilisateur_id=utilisateur_id,
            id=id,
            date_creation=date_creation
        )

    @classmethod
    def tous(cls, db):
        lignes = db.selectionner(
            """SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id
               FROM incident ORDER BY date_creation DESC"""
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]

    @classmethod
    def trouver_par_id(cls, db, id):
        lignes = db.selectionner(
            """SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id
               FROM incident WHERE id=%s""",
            (id,)
        )
        return cls._depuis_ligne(lignes[0]) if lignes else None

    @classmethod
    def trouver_par_statut(cls, db, statut):
        lignes = db.selectionner(
            """SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id
               FROM incident WHERE statut=%s ORDER BY date_creation DESC""",
            (statut,)
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]

    @classmethod
    def trouver_par_priorite(cls, db, priorite):
        lignes = db.selectionner(
            """SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id
               FROM incident WHERE priorite=%s ORDER BY date_creation DESC""",
            (priorite,)
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]

    @classmethod
    def trouver_par_utilisateur(cls, db, utilisateur_id):
        """Tous les incidents signalés par un utilisateur donné"""
        lignes = db.selectionner(
            """SELECT id, titre, description, priorite, statut, date_creation, utilisateur_id
               FROM incident WHERE utilisateur_id=%s ORDER BY date_creation DESC""",
            (utilisateur_id,)
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]

    @classmethod
    def compter_par_statut(cls, db):
        """Statistiques : nombre d'incidents par statut"""
        lignes = db.selectionner(
            "SELECT statut, COUNT(*) FROM incident GROUP BY statut"
        )
        return {statut: nb for statut, nb in lignes}


