from datetime import datetime


class Intervention:
    def __init__(self, commentaire, incident_id, technicien_id,
                 duree_minutes=0, id=None, date_intervention=None):
        self.id = id
        self.commentaire = commentaire
        self.duree_minutes = duree_minutes
        self.incident_id = incident_id
        self.technicien_id = technicien_id
        self.date_intervention = date_intervention or datetime.now()

        self._valider()

    # --- Validation ---
    def _valider(self):
        if not self.commentaire or not self.commentaire.strip():
            raise ValueError("Le commentaire est obligatoire")

        if self.incident_id is None:
            raise ValueError("L'incident_id est obligatoire")

        if self.technicien_id is None:
            raise ValueError("Le technicien_id est obligatoire")

        if not isinstance(self.duree_minutes, int) or self.duree_minutes < 0:
            raise ValueError("La durée doit être un entier positif ou nul")

    # --- Représentation ---
    def __repr__(self):
        return (f"Intervention(id={self.id}, incident_id={self.incident_id}, "
                f"technicien_id={self.technicien_id}, duree={self.duree_minutes}min)")

    def __str__(self):
        return f"Intervention #{self.id} ({self.duree_minutes} min) - {self.commentaire[:40]}..."

    # --- Sauvegarde (insertion ou mise à jour) ---
    def sauvegarder(self, db):
        if self.id is None:
            self.id = db.executer(
                """INSERT INTO intervention (commentaire, duree_minutes, date_intervention,
                                              incident_id, technicien_id)
                   VALUES (%s, %s, %s, %s, %s)""",
                (self.commentaire, self.duree_minutes, self.date_intervention,
                 self.incident_id, self.technicien_id)
            )
        else:
            db.executer(
                """UPDATE intervention
                   SET commentaire=%s, duree_minutes=%s, incident_id=%s, technicien_id=%s
                   WHERE id=%s""",
                (self.commentaire, self.duree_minutes,
                 self.incident_id, self.technicien_id, self.id)
            )
        return self.id

    def supprimer(self, db):
        if self.id is None:
            raise ValueError("Impossible de supprimer une intervention sans id")
        db.executer("DELETE FROM intervention WHERE id=%s", (self.id,))

    # --- Relations (récupérer les objets liés) ---
    def get_incident(self, db):
        from .Incident import Incident
        return Incident.trouver_par_id(db, self.incident_id)

    def get_technicien(self, db):
        from .Utilisateur import Utilisateur
        return Utilisateur.trouver_par_id(db, self.technicien_id)

    # --- Méthodes de classe pour la lecture ---
    @classmethod
    def _depuis_ligne(cls, ligne):
        id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id = ligne
        return cls(
            commentaire=commentaire,
            duree_minutes=duree_minutes,
            incident_id=incident_id,
            technicien_id=technicien_id,
            id=id,
            date_intervention=date_intervention
        )

    @classmethod
    def tous(cls, db):
        lignes = db.selectionner(
            """SELECT id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id
               FROM intervention"""
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]

    @classmethod
    def trouver_par_id(cls, db, id):
        lignes = db.selectionner(
            """SELECT id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id
               FROM intervention WHERE id=%s""",
            (id,)
        )
        return cls._depuis_ligne(lignes[0]) if lignes else None

    @classmethod
    def trouver_par_incident(cls, db, incident_id):
        """Toutes les interventions liées à un incident donné"""
        lignes = db.selectionner(
            """SELECT id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id
               FROM intervention WHERE incident_id=%s
               ORDER BY date_intervention""",
            (incident_id,)
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]

    @classmethod
    def trouver_par_technicien(cls, db, technicien_id):
        """Toutes les interventions faites par un technicien donné"""
        lignes = db.selectionner(
            """SELECT id, commentaire, duree_minutes, date_intervention, incident_id, technicien_id
               FROM intervention WHERE technicien_id=%s
               ORDER BY date_intervention DESC""",
            (technicien_id,)
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]


    @classmethod
    def duree_totale_par_incident(cls, db, incident_id):
        """Somme du temps passé (en minutes) sur un incident"""
        resultat = db.selectionner(
            "SELECT SUM(duree_minutes) FROM intervention WHERE incident_id=%s",
            (incident_id,)
        )
        total = resultat[0][0]
        return total if total is not None else 0

    @classmethod
    def duree_totale_par_technicien(cls, db, technicien_id):
        """Somme du temps passé par un technicien, tous incidents confondus"""
        resultat = db.selectionner(
            "SELECT SUM(duree_minutes) FROM intervention WHERE technicien_id=%s",
            (technicien_id,)
        )
        total = resultat[0][0]
        return total if total is not None else 0