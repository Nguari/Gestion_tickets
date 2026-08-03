import re
from datetime import date


class Utilisateur:
    ROLES_VALIDES = ("UTILISATEUR", "TECHNICIEN", "ADMIN")

    def __init__(self, login, password, nom, prenom, email,
                 role="UTILISATEUR", service=None, id=None, date_creation=None):
        self.id = id
        self.login = login
        self.password = password
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.role = role
        self.service = service
        self.date_creation = date_creation or date.today()

        self._valider()

    # --- Validation ---
    def _valider(self):
        if not self.login or not self.login.strip():
            raise ValueError("Le login est obligatoire")

        if not self.password or not self.password.strip():
            raise ValueError("Le mot de passe est obligatoire")

        if not self.nom or not self.nom.strip():
            raise ValueError("Le nom est obligatoire")

        if not self.prenom or not self.prenom.strip():
            raise ValueError("Le prénom est obligatoire")

        if not self._email_valide(self.email):
            raise ValueError(f"Email invalide : {self.email}")

        if self.role not in self.ROLES_VALIDES:
            raise ValueError(f"Rôle invalide : {self.role}. Doit être parmi {self.ROLES_VALIDES}")

    @staticmethod
    def _email_valide(email):
        if not email:
            return False
        motif = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        return re.match(motif, email) is not None

    # --- Représentation ---
    def __repr__(self):
        return (f"Utilisateur(id={self.id}, login='{self.login}', "
                f"nom='{self.nom}', prenom='{self.prenom}', role='{self.role}')")

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.login}) - {self.role}"

    # --- Sauvegarde (insertion ou mise à jour) ---
    def sauvegarder(self, db):
        if self.id is None:
            self.id = db.executer(
                """INSERT INTO utilisateur (login, password, nom, prenom, email, role, service, date_creation)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (self.login, self.password, self.nom, self.prenom,
                 self.email, self.role, self.service, self.date_creation)
            )
        else:
            db.executer(
                """UPDATE utilisateur
                   SET login=%s, password=%s, nom=%s, prenom=%s, email=%s, role=%s, service=%s
                   WHERE id=%s""",
                (self.login, self.password, self.nom, self.prenom,
                 self.email, self.role, self.service, self.id)
            )
        return self.id

    def supprimer(self, db):
        if self.id is None:
            raise ValueError("Impossible de supprimer un utilisateur sans id")
        db.executer("DELETE FROM utilisateur WHERE id=%s", (self.id,))

    # --- Méthodes de classe pour la lecture ---
    @classmethod
    def _depuis_ligne(cls, ligne):
        """Convertit une ligne SQL (tuple) en objet Utilisateur"""
        id, login, password, nom, prenom, email, role, service, date_creation = ligne
        return cls(
            login=login, password=password, nom=nom, prenom=prenom,
            email=email, role=role, service=service,
            id=id, date_creation=date_creation
        )

    @classmethod
    def tous(cls, db):
        lignes = db.selectionner(
            "SELECT id, login, password, nom, prenom, email, role, service, date_creation FROM utilisateur"
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]

    @classmethod
    def trouver_par_id(cls, db, id):
        lignes = db.selectionner(
            "SELECT id, login, password, nom, prenom, email, role, service, date_creation "
            "FROM utilisateur WHERE id=%s",
            (id,)
        )
        return cls._depuis_ligne(lignes[0]) if lignes else None

    @classmethod
    def trouver_par_login(cls, db, login):
        lignes = db.selectionner(
            "SELECT id, login, password, nom, prenom, email, role, service, date_creation "
            "FROM utilisateur WHERE login=%s",
            (login,)
        )
        return cls._depuis_ligne(lignes[0]) if lignes else None

    @classmethod
    def trouver_par_role(cls, db, role):
        lignes = db.selectionner(
            "SELECT id, login, password, nom, prenom, email, role, service, date_creation "
            "FROM utilisateur WHERE role=%s",
            (role,)
        )
        return [cls._depuis_ligne(ligne) for ligne in lignes]

    # --- Authentification simple ---
    @classmethod
    def authentifier(cls, db, login, password):
        utilisateur = cls.trouver_par_login(db, login)
        if utilisateur and utilisateur.password == password:
            return utilisateur
        return None