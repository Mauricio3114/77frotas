from app import db


class Marca(db.Model):
    __tablename__ = "marcas"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(100),
        nullable=False
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