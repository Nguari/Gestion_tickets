from database import Connexion


def create_tables():
    with Connexion() as db:
        if db.connection is None:
            print(" Connexion échouée")
            return

        db.executer("""
            CREATE TABLE IF NOT EXISTS utilisateur (
                id INT AUTO_INCREMENT PRIMARY KEY,
                login VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                nom VARCHAR(100) NOT NULL,
                prenom VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL,
                role ENUM('UTILISATEUR', 'TECHNICIEN', 'ADMIN') NOT NULL DEFAULT 'UTILISATEUR',
                service VARCHAR(100),
                date_creation DATE NOT NULL DEFAULT (CURRENT_DATE),
                CONSTRAINT chk_email_format CHECK (email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Za-z]{2,}$')
            )
        """)
        print(" Table 'utilisateur' créée")

        db.executer("""
            CREATE TABLE IF NOT EXISTS incident (
                id INT AUTO_INCREMENT PRIMARY KEY,
                titre VARCHAR(150) NOT NULL,
                description TEXT NOT NULL,
                priorite ENUM('BASSE', 'MOYENNE', 'HAUTE', 'CRITIQUE') NOT NULL DEFAULT 'MOYENNE',
                statut ENUM('OUVERT', 'EN_COURS', 'RESOLU', 'FERME') NOT NULL DEFAULT 'OUVERT',
                date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                utilisateur_id INT NOT NULL,
                CONSTRAINT fk_incident_utilisateur
                    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            )
        """)
        print(" Table 'incident' créée")

        db.executer("""
            CREATE TABLE IF NOT EXISTS intervention (
                id INT AUTO_INCREMENT PRIMARY KEY,
                commentaire TEXT NOT NULL,
                duree_minutes INT NOT NULL DEFAULT 0,
                date_intervention DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                incident_id INT NOT NULL,
                technicien_id INT NOT NULL,
                CONSTRAINT chk_duree_positive CHECK (duree_minutes >= 0),
                CONSTRAINT fk_intervention_incident
                    FOREIGN KEY (incident_id) REFERENCES incident(id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT fk_intervention_technicien
                    FOREIGN KEY (technicien_id) REFERENCES utilisateur(id)
                    ON DELETE RESTRICT ON UPDATE CASCADE
            )
        """)
        print(" Table 'intervention' créée")


if __name__ == "__main__":
    create_tables()