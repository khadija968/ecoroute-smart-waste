from datetime import datetime, timezone
from models import db


class Tournee(db.Model):
    __tablename__ = "tournees"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    camion_id = db.Column(db.Integer, db.ForeignKey("camions.id"), nullable=False)
    depot_id = db.Column(db.Integer, db.ForeignKey("depots.id"), nullable=False)
    distance_km = db.Column(db.Float, nullable=False, default=0.0)
    charge_kg = db.Column(db.Float, nullable=False, default=0.0)
    taux_remplissage_camion = db.Column(db.Float, nullable=False, default=0.0)
    duree_estimee_min = db.Column(db.Float, nullable=False, default=0.0)
    co2_kg = db.Column(db.Float, nullable=False, default=0.0)
    statut = db.Column(
        db.Enum("planifiee", "en_cours", "terminee", name="tournee_statuts"),
        nullable=False,
        default="planifiee",
    )
    algorithme = db.Column(db.String(50), nullable=False, default="ortools_vrp")
    cree_par = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    camion = db.relationship("Camion", lazy="joined")
    depot = db.relationship("Depot", lazy="joined")
    points = db.relationship(
        "TourneePoint",
        back_populates="tournee",
        order_by="TourneePoint.ordre",
        cascade="all, delete-orphan",
    )

    def to_dict(self, include_points: bool = False) -> dict:
        data = {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "camion_id": self.camion_id,
            "camion_nom": self.camion.nom if self.camion else None,
            "depot_id": self.depot_id,
            "distance_km": self.distance_km,
            "charge_kg": self.charge_kg,
            "taux_remplissage_camion": self.taux_remplissage_camion,
            "duree_estimee_min": self.duree_estimee_min,
            "co2_kg": self.co2_kg,
            "statut": self.statut,
            "algorithme": self.algorithme,
            "cree_par": self.cree_par,
        }
        if include_points:
            data["points"] = [p.to_dict() for p in self.points]
        return data


class TourneePoint(db.Model):
    __tablename__ = "tournee_points"

    id = db.Column(db.Integer, primary_key=True)
    tournee_id = db.Column(db.Integer, db.ForeignKey("tournees.id"), nullable=False)
    point_id = db.Column(
        db.Integer, db.ForeignKey("points_collecte.id"), nullable=False
    )
    ordre = db.Column(db.Integer, nullable=False)
    collecte = db.Column(db.Boolean, nullable=False, default=False)
    kg_reel = db.Column(db.Float, nullable=True)
    heure_passage = db.Column(db.DateTime, nullable=True)

    tournee = db.relationship("Tournee", back_populates="points")
    point = db.relationship("PointCollecte", lazy="joined")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tournee_id": self.tournee_id,
            "point_id": self.point_id,
            "point_nom": self.point.nom if self.point else None,
            "lat": self.point.lat if self.point else None,
            "lng": self.point.lng if self.point else None,
            "kg_estime": self.point.kg_estime if self.point else None,
            "priorite": self.point.priorite if self.point else None,
            "ordre": self.ordre,
            "collecte": self.collecte,
            "kg_reel": self.kg_reel,
            "heure_passage": (
                self.heure_passage.isoformat() if self.heure_passage else None
            ),
        }