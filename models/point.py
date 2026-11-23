from models import db


class PointCollecte(db.Model):
    __tablename__ = "points_collecte"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    type = db.Column(
        db.Enum(
            "conteneur",
            "marche",
            "hopital",
            "ecole",
            "gare",
            "quartier",
            "decharge_sauvage",
            name="point_types",
        ),
        nullable=False,
        default="conteneur",
    )
    kg_estime = db.Column(db.Float, nullable=False, default=0.0)
    niveau_remplissage = db.Column(
        db.Enum("vide", "moyen", "plein", "debordant", name="niveaux_remplissage"),
        nullable=False,
        default="moyen",
    )
    priorite = db.Column(
        db.Enum("haute", "moyenne", "basse", name="priorites"),
        nullable=False,
        default="moyenne",
    )
    priorite_mode = db.Column(
        db.Enum("manuelle", "automatique", name="priorite_modes"),
        nullable=False,
        default="automatique",
    )
    derniere_collecte = db.Column(db.DateTime, nullable=True)
    taux_remplissage_pct = db.Column(db.Float, nullable=False, default=50.0)
    actif = db.Column(db.Boolean, nullable=False, default=True)
    fenetre_debut = db.Column(db.Time, nullable=True)
    fenetre_fin = db.Column(db.Time, nullable=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "lat": self.lat,
            "lng": self.lng,
            "type": self.type,
            "kg_estime": self.kg_estime,
            "niveau_remplissage": self.niveau_remplissage,
            "priorite": self.priorite,
            "priorite_mode": self.priorite_mode,
            "derniere_collecte": (
                self.derniere_collecte.isoformat() if self.derniere_collecte else None
            ),
            "taux_remplissage_pct": self.taux_remplissage_pct,
            "actif": self.actif,
            "fenetre_debut": (
                self.fenetre_debut.strftime("%H:%M") if self.fenetre_debut else None
            ),
            "fenetre_fin": (
                self.fenetre_fin.strftime("%H:%M") if self.fenetre_fin else None
            ),
        }