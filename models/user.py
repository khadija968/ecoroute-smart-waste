from datetime import datetime, timezone
import bcrypt
from models import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum("admin", "operateur", "chauffeur", name="user_roles"),
        nullable=False,
        default="operateur",
    )
    actif = db.Column(db.Boolean, nullable=False, default=True)
    cree_le = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, mot_de_passe: str) -> None:
        hashed = bcrypt.hashpw(mot_de_passe.encode("utf-8"), bcrypt.gensalt())
        self.mot_de_passe_hash = hashed.decode("utf-8")

    def check_password(self, mot_de_passe: str) -> bool:
        return bcrypt.checkpw(
            mot_de_passe.encode("utf-8"),
            self.mot_de_passe_hash.encode("utf-8"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nom": self.nom,
            "email": self.email,
            "role": self.role,
            "actif": self.actif,
            "cree_le": self.cree_le.isoformat() if self.cree_le else None,
        }