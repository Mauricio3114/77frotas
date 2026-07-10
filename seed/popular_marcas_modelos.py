import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from app import create_app, db
from app.models.marca import Marca
from app.models.modelo import Modelo


app = create_app()

marcas = {

    "Chevrolet":[
        "Onix",
        "Onix Plus",
        "Joy",
        "Prisma",
        "Cruze",
        "Tracker",
        "Spin",
        "Montana",
        "S10",
        "Trailblazer"
    ],

    "Fiat":[
        "Mobi",
        "Uno",
        "Argo",
        "Cronos",
        "Pulse",
        "Fastback",
        "Toro",
        "Strada",
        "Fiorino",
        "Doblo",
        "Ducato"
    ],

    "Volkswagen":[
        "Gol",
        "Fox",
        "Polo",
        "Virtus",
        "Nivus",
        "T-Cross",
        "Taos",
        "Saveiro",
        "Amarok"
    ],

    "Toyota":[
        "Etios",
        "Yaris",
        "Corolla",
        "Corolla Cross",
        "Hilux",
        "SW4",
        "Prius"
    ],

    "Honda":[
        "Fit",
        "City",
        "Civic",
        "HR-V",
        "WR-V",
        "CR-V"
    ],

    "Hyundai":[
        "HB20",
        "HB20S",
        "Creta",
        "Tucson",
        "Santa Fé",
        "Azera"
    ],

    "Renault":[
        "Kwid",
        "Sandero",
        "Logan",
        "Oroch",
        "Duster",
        "Master"
    ],

    "Nissan":[
        "March",
        "Versa",
        "Sentra",
        "Kicks",
        "Frontier"
    ],

    "Jeep":[
        "Renegade",
        "Compass",
        "Commander",
        "Gladiator"
    ],

    "Ford":[
        "Ka",
        "Ka Sedan",
        "EcoSport",
        "Territory",
        "Ranger",
        "Transit"
    ],

    "Peugeot":[
        "208",
        "2008",
        "3008",
        "Partner"
    ],

    "Citroën":[
        "C3",
        "C3 Aircross",
        "Basalt",
        "Jumpy",
        "Jumper"
    ],

    "BYD":[
        "Dolphin Mini",
        "Dolphin",
        "Seal",
        "Yuan Pro",
        "Yuan Plus",
        "Song Pro",
        "Song Plus",
        "Han",
        "Shark"
    ],

    "GWM":[
        "Ora 03 Skin",
        "Ora 03 GT",
        "Haval H6 HEV",
        "Haval H6 PHEV",
        "Tank 300"
    ],

    "CAOA Chery":[
        "iCar",
        "Arrizo 5",
        "Arrizo 6",
        "Tiggo 2",
        "Tiggo 3X",
        "Tiggo 5X",
        "Tiggo 7",
        "Tiggo 8"
    ],

    "JAC":[
        "E-JS1",
        "E-JS4",
        "E-J7",
        "T40",
        "T50"
    ],

    "BMW":[
        "320i",
        "330e",
        "X1",
        "X3",
        "X5",
        "i3",
        "i4",
        "i5",
        "i7",
        "iX1",
        "iX3",
        "iX"
    ],

    "Mercedes-Benz":[
        "Classe A",
        "Classe C",
        "Classe E",
        "GLA",
        "GLB",
        "GLC",
        "GLE",
        "Sprinter",
        "EQA",
        "EQB",
        "EQE",
        "EQS"
    ],

    "Audi":[
        "A3",
        "A4",
        "A5",
        "Q3",
        "Q5",
        "Q7",
        "Q4 e-tron",
        "Q8 e-tron",
        "e-tron GT"
    ],

    "Volvo":[
        "XC40",
        "XC60",
        "XC90",
        "EX30",
        "EX40",
        "EC40"
    ],

    "Porsche":[
        "Macan",
        "Cayenne",
        "911",
        "Panamera",
        "Taycan",
        "Macan Electric"
    ],

    "RAM":[
        "Rampage",
        "1500",
        "2500",
        "3500"
    ],

    "Mitsubishi":[
        "L200 Triton",
        "Pajero Sport",
        "Outlander",
        "Eclipse Cross"
    ],

    "Kia":[
        "Sportage",
        "Sorento",
        "Cerato",
        "Stonic",
        "Niro"
    ],

    "Suzuki":[
        "Jimny",
        "Vitara",
        "S-Cross"
    ],

    "Lexus":[
        "UX",
        "NX",
        "RX",
        "ES",
        "LS"
    ]

        ,

    "Volvo Caminhões":[
        "VM",
        "VMX",
        "FH",
        "FM",
        "FMX"
    ],

    "Scania":[
        "P250",
        "P280",
        "P320",
        "G360",
        "G410",
        "R450",
        "R500",
        "R540",
        "S500",
        "S540"
    ],

    "DAF":[
        "XF",
        "CF",
        "LF"
    ],

    "Iveco":[
        "Daily",
        "Tector",
        "Hi-Way",
        "S-Way"
    ],

    "Volkswagen Caminhões":[
        "Delivery",
        "Worker",
        "Constellation",
        "Meteor"
    ],

    "Agrale":[
        "A8700",
        "A10000"
    ],

    "Marcopolo":[
        "Senior",
        "Viaggio",
        "Paradiso"
    ],

    "Comil":[
        "Campione",
        "Invictus"
    ],

    "Mascarello":[
        "GranVia",
        "Roma"
    ],

    "Caio":[
        "Apache Vip",
        "Millennium"
    ],

    "Busscar":[
        "Vissta Buss",
        "El Buss"
    ],

    "Land Rover":[
        "Defender",
        "Discovery",
        "Discovery Sport",
        "Range Rover Evoque",
        "Range Rover Velar",
        "Range Rover Sport"
    ],

    "Mini":[
        "Cooper",
        "Cooper S",
        "Cooper E",
        "Cooper SE",
        "Aceman"
    ]

}

with app.app_context():

    for nome_marca, lista_modelos in marcas.items():

        marca = Marca.query.filter_by(
            nome=nome_marca
        ).first()

        if not marca:

            marca = Marca(
                nome=nome_marca,
                ativo=True
            )

            db.session.add(marca)
            db.session.flush()

        for nome_modelo in lista_modelos:

            existe = Modelo.query.filter_by(
                marca_id=marca.id,
                nome=nome_modelo
            ).first()

            if not existe:

                db.session.add(

                    Modelo(
                        marca_id=marca.id,
                        nome=nome_modelo,
                        ativo=True
                    )

                )

    db.session.commit()

print("Marcas e modelos cadastrados com sucesso.")