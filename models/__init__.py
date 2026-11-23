from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.depot import Depot
from models.point import PointCollecte
from models.camion import Camion
from models.tournee import Tournee, TourneePoint
from models.parametre import Parametre

__all__ = [
    "db",
    "User",
    "Depot",
    "PointCollecte",
    "Camion",
    "Tournee",
    "TourneePoint",
    "Parametre",
]