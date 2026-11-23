from models import db


class Parametre(db.Model):
    __tablename__ = "parametres"

    cle = db.Column(db.String(100), primary_key=True)
    valeur = db.Column(db.String(255), nullable=False)

    def to_dict(self) -> dict:
        return {"cle": self.cle, "valeur": self.valeur}