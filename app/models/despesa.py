from datetime import date
from app import db


class Despesa(db.Model):
    __tablename__ = "despesas"

    id = db.Column(db.Integer, primary_key=True)

    conta_id = db.Column(
        db.Integer,
        db.ForeignKey("contas.id"),
        nullable=False
    )

    veiculo_id = db.Column(
        db.Integer,
        db.ForeignKey("veiculos.id"),
        nullable=False
    )

    tipo = db.Column(
        db.String(50),
        nullable=False
    )

    valor = db.Column(
        db.Numeric(10,2),
        nullable=False
    )

    data = db.Column(
        db.Date,
        default=date.today
    )

    observacoes = db.Column(db.Text)

    conta = db.relationship(
        "Conta",
        backref="despesas"
    )

    veiculo = db.relationship(
        "Veiculo",
        backref="despesas"
    )