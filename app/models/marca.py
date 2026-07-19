from app import db


class Marca(db.Model):
    __tablename__ = "marcas"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    fabricante = db.Column(db.String(150))

    pais_origem = db.Column(db.String(100))

    segmento = db.Column(
        db.String(50)
    )
    # Passeio
    # Caminhão
    # Moto
    # Ônibus
    # Utilitário
    # Agrícola
    # Multimarca

    logo = db.Column(db.String(255))

    cor = db.Column(db.String(20))

    ordem = db.Column(
        db.Integer,
        default=0
    )

    ativo = db.Column(
        db.Boolean,
        default=True
    )

    modelos = db.relationship(
        "Modelo",
        backref="marca",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return self.nome