from models import db


class Camion(db.Model):
    __tablename__ = "camions"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    capacite_kg = db.Column(db.Float, nullable=False)
    statut = db.Column(
        db.Enum("disponible", "maintenance", "en_tournee", name="camion_statuts"),
        nullable=False,
        default="disponible",
    )
    km_total = db.Column(db.Float, nullable=False, default=0.0)
    date_derniere_maintenance = db.Column(db.DateTime, nullable=True)
    seuil_maintenance_km = db.Column(db.Float, nullable=False, default=10000.0)
    conso_l_100km = db.Column(db.Float, nullable=False, default=28.0)
    chauffeur_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    chauffeur = db.relationship("User", foreign_keys=[chauffeur_id], lazy="joined")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "capacite_kg": self.capacite_kg,
            "statut": self.statut,
            "km_total": self.km_total,
            "date_derniere_maintenance": (
                self.date_derniere_maintenance.isoformat()
                if self.date_derniere_maintenance
                else None
            ),
            "seuil_maintenance_km": self.seuil_maintenance_km,
            "conso_l_100km": self.conso_l_100km,
            "chauffeur_id": self.chauffeur_id,
            "chauffeur_nom": self.chauffeur.nom if self.chauffeur else None,
        }