from app import create_app, db

from app.models.marca import Marca
from app.models.modelo import Modelo

app = create_app()

BASE = {

    "Chevrolet": [
        ("Onix", "Hatch"),
        ("Onix Plus", "Sedan"),
        ("Tracker", "SUV"),
        ("Spin", "Minivan"),
        ("Montana", "Pickup"),
        ("S10", "Pickup"),
        ("Trailblazer", "SUV"),
    ],

    "Fiat": [
        ("Argo", "Hatch"),
        ("Mobi", "Hatch"),
        ("Cronos", "Sedan"),
        ("Toro", "Pickup"),
        ("Pulse", "SUV"),
        ("Fastback", "SUV"),
        ("Strada", "Pickup"),
        ("Fiorino", "Utilitário"),
    ],

    "Volkswagen": [
        ("Gol", "Hatch"),
        ("Polo", "Hatch"),
        ("Virtus", "Sedan"),
        ("Nivus", "SUV"),
        ("T-Cross", "SUV"),
        ("Taos", "SUV"),
        ("Saveiro", "Pickup"),
        ("Amarok", "Pickup"),
    ],

    "Toyota": [
        ("Corolla", "Sedan"),
        ("Corolla Cross", "SUV"),
        ("Hilux", "Pickup"),
        ("SW4", "SUV"),
        ("Yaris", "Hatch"),
    ],

    "Hyundai": [
        ("HB20", "Hatch"),
        ("HB20S", "Sedan"),
        ("Creta", "SUV"),
    ],

    "Honda": [
        ("City", "Sedan"),
        ("Civic", "Sedan"),
        ("HR-V", "SUV"),
        ("WR-V", "SUV"),
    ],

}

with app.app_context():

    for nome_marca, modelos in BASE.items():

        marca = Marca.query.filter_by(
            nome=nome_marca
        ).first()

        if not marca:

            marca = Marca(
                nome=nome_marca
            )

            db.session.add(marca)
            db.session.flush()

        for nome_modelo, categoria in modelos:

            existe = Modelo.query.filter_by(
                marca_id=marca.id,
                nome=nome_modelo
            ).first()

            if existe:
                continue

            db.session.add(

                Modelo(

                    marca_id=marca.id,

                    nome=nome_modelo,

                    categoria=categoria

                )

            )

    db.session.commit()

print("Base cadastrada com sucesso!")