from datetime import datetime, timedelta, timezone
from app import create_app
from models import db, User, Depot, PointCollecte, Camion, Parametre


def seed_database():
    app = create_app()
    with app.app_context():
        db.create_all()

        # 1. Utilisateurs (si vide)
        if User.query.count() == 0:
            admin = User(nom="Responsable Proprete", email="admin@ecoroute.ma", role="admin")
            admin.set_password("admin123")

            operateur = User(nom="Agent Commune", email="operateur@ecoroute.ma", role="operateur")
            operateur.set_password("operateur123")

            ch1 = User(nom="Hassan Benali", email="chauffeur1@ecoroute.ma", role="chauffeur")
            ch1.set_password("chauffeur123")

            ch2 = User(nom="Youssef Amrani", email="chauffeur2@ecoroute.ma", role="chauffeur")
            ch2.set_password("chauffeur123")

            ch3 = User(nom="Karim Idrissi", email="chauffeur3@ecoroute.ma", role="chauffeur")
            ch3.set_password("chauffeur123")

            db.session.add_all([admin, operateur, ch1, ch2, ch3])
            db.session.flush()
        else:
            ch1 = User.query.filter_by(email="chauffeur1@ecoroute.ma").first()
            ch2 = User.query.filter_by(email="chauffeur2@ecoroute.ma").first()
            ch3 = User.query.filter_by(email="chauffeur3@ecoroute.ma").first()

        # 2. Dépôt central (Taroudant)
        if Depot.query.count() == 0:
            depot = Depot(
                nom="Dépôt Central Taroudant",
                lat=30.4620,
                lng=-8.8500,
                ville="Taroudant",
            )
            db.session.add(depot)

        # 3. Camions (3 camions de démo)
        if Camion.query.count() == 0:
            camions = [
                Camion(
                    nom="Camion Benne 01",
                    capacite_kg=1200.0,
                    statut="disponible",
                    km_total=4200.0,
                    seuil_maintenance_km=10000.0,
                    conso_l_100km=26.0,
                    chauffeur_id=ch1.id if ch1 else None,
                ),
                Camion(
                    nom="Camion Benne 02",
                    capacite_kg=1500.0,
                    statut="disponible",
                    km_total=6100.0,
                    seuil_maintenance_km=10000.0,
                    conso_l_100km=29.0,
                    chauffeur_id=ch2.id if ch2 else None,
                ),
                Camion(
                    nom="Camion Grand Volume 03",
                    capacite_kg=2000.0,
                    statut="disponible",
                    km_total=2800.0,
                    seuil_maintenance_km=12000.0,
                    conso_l_100km=33.0,
                    chauffeur_id=ch3.id if ch3 else None,
                ),
            ]
            db.session.add_all(camions)

        # 4. 15 Points de collecte à Taroudant
        if PointCollecte.query.count() == 0:
            now = datetime.now(timezone.utc)
            points_data = [
                ("Hôpital Mokhtar Soussi", 30.4718, -8.8745, "hopital", 320, "debordant", "haute", 95, 4),
                ("Souk Jdid (Grand Marché)", 30.4705, -8.8780, "marche", 450, "debordant", "haute", 92, 3),
                ("Marché Bab Zorgane", 30.4675, -8.8722, "marche", 380, "plein", "haute", 85, 3),
                ("Place Assarag", 30.4709, -8.8762, "quartier", 240, "plein", "moyenne", 75, 2),
                ("Gare Routière Taroudant", 30.4755, -8.8685, "gare", 290, "plein", "haute", 80, 3),
                ("Lycée Ibnou Soulaimane", 30.4690, -8.8825, "ecole", 160, "moyen", "moyenne", 55, 2),
                ("Quartier El Kasbah", 30.4742, -8.8810, "quartier", 210, "moyen", "moyenne", 60, 2),
                ("Quartier Mahatta", 30.4650, -8.8640, "quartier", 180, "moyen", "moyenne", 50, 1),
                ("Bab El Khemis", 30.4775, -8.8740, "conteneur", 270, "plein", "haute", 82, 4),
                ("Avenue Mohammed V", 30.4680, -8.8695, "conteneur", 140, "moyen", "basse", 45, 1),
                ("Quartier Sidi Belkacem", 30.4638, -8.8790, "quartier", 190, "moyen", "moyenne", 55, 2),
                ("École Al Amal", 30.4730, -8.8615, "ecole", 110, "vide", "basse", 25, 1),
                ("Zone Industrielle Sud", 30.4585, -8.8560, "decharge_sauvage", 400, "debordant", "haute", 96, 5),
                ("Bab Targhount", 30.4660, -8.8860, "conteneur", 150, "moyen", "basse", 40, 1),
                ("Hay Hassani", 30.4610, -8.8670, "quartier", 220, "plein", "moyenne", 70, 2),
            ]
            for nom, lat, lng, ptype, kg, niv, prio, taux, jours in points_data:
                db.session.add(
                    PointCollecte(
                        nom=nom,
                        lat=lat,
                        lng=lng,
                        type=ptype,
                        kg_estime=float(kg),
                        niveau_remplissage=niv,
                        priorite=prio,
                        priorite_mode="automatique",
                        taux_remplissage_pct=float(taux),
                        derniere_collecte=now - timedelta(days=jours),
                        actif=True,
                    )
                )

        # 5. Paramètres par défaut
        defaults = {
            "poids_remplissage": "0.40",
            "poids_jours": "0.25",
            "poids_type": "0.20",
            "poids_kg": "0.15",
            "seuil_haute": "70",
            "seuil_moyenne": "40",
            "vitesse_moyenne_kmh": "30",
            "algorithme_defaut": "ortools_vrp",
            "rayon_ville_km": "25",
            "co2_kg_par_litre": "2.68",
        }
        for cle, valeur in defaults.items():
            if not db.session.get(Parametre, cle):
                db.session.add(Parametre(cle=cle, valeur=valeur))

        db.session.commit()
        print("Base MySQL initialisee avec succes (Taroudant : 1 depot, 15 points, 3 camions, 5 users) !")


if __name__ == "__main__":
    seed_database()