from models import db


class Depot(db.Model):
    __tablename__ = "depots"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    ville = db.Column(db.String(100), nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "lat": self.lat,
            "lng": self.lng,
            "ville": self.ville,
        }