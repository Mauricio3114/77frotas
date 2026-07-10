from datetime import datetime

from app import db


class Negociacao(db.Model):
    __tablename__ = "negociacoes"

    id = db.Column(db.Integer, primary_key=True)

    conta_id = db.Column(
        db.Integer,
        db.ForeignKey("contas.id"),
        nullable=False
    )

    parcela_id = db.Column(
        db.Integer,
        db.ForeignKey("parcelas.id"),
        nullable=False
    )

    valor_original = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    novo_valor = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    vencimento_original = db.Column(
        db.Date,
        nullable=False
    )

    novo_vencimento = db.Column(
        db.Date,
        nullable=False
    )

    juros = db.Column(
        db.Numeric(10,2),
        default=0
    )

    multa = db.Column(
        db.Numeric(10,2),
        default=0
    )

    desconto = db.Column(
        db.Numeric(10,2),
        default=0
    )

    observacoes = db.Column(db.Text)

    status = db.Column(
        db.String(30),
        default="ativa"
    )
    # ativa
    # cancelada
    # concluida

    data_negociacao = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    conta = db.relationship(
        "Conta",
        backref="negociacoes"
    )

    parcela = db.relationship(
        "Parcela",
        backref="negociacoes"
    )

    def __repr__(self):
        return f"Negociação {self.id}"