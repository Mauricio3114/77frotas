from datetime import datetime
from app import db


class Locacao(db.Model):
    __tablename__ = "locacoes"

    id = db.Column(db.Integer, primary_key=True)

    conta_id = db.Column(
        db.Integer,
        db.ForeignKey("contas.id"),
        nullable=False
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    veiculo_id = db.Column(
        db.Integer,
        db.ForeignKey("veiculos.id"),
        nullable=False
    )

    data_inicio = db.Column(
        db.Date,
        nullable=False
    )

    data_fim = db.Column(db.Date)

    plano = db.Column(
        db.String(20),
        nullable=False
    )
    # diaria
    # semanal
    # quinzenal
    # mensal

    valor_diaria = db.Column(
        db.Numeric(10,2),
        default=0
    )

    valor_caucao = db.Column(
        db.Numeric(10,2),
        default=0
    )

    dia_vencimento = db.Column(db.Integer)

    status = db.Column(
        db.String(30),
        default="ativa"
    )
    # ativa
    # encerrada
    # cancelada

    observacoes = db.Column(db.Text)

    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    conta = db.relationship(
        "Conta",
        backref="locacoes"
    )

    cliente = db.relationship(
        "Cliente",
        backref="locacoes"
    )

    veiculo = db.relationship(
        "Veiculo",
        backref="locacoes"
    )