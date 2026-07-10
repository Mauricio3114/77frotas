from datetime import datetime
from app import db


class Parcela(db.Model):
    __tablename__ = "parcelas"

    id = db.Column(db.Integer, primary_key=True)

    # Conta
    conta_id = db.Column(
        db.Integer,
        db.ForeignKey("contas.id"),
        nullable=False
    )

    # Locação
    locacao_id = db.Column(
        db.Integer,
        db.ForeignKey("locacoes.id"),
        nullable=False
    )

    # Dados da Parcela
    numero = db.Column(
        db.Integer,
        nullable=False
    )

    vencimento = db.Column(
        db.Date,
        nullable=False
    )

    valor = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    # Recebimento
    valor_recebido = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    data_pagamento = db.Column(
        db.Date
    )

    forma_pagamento = db.Column(
        db.String(40)
    )

    juros = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    multa = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    desconto = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    # Situação
    status = db.Column(
        db.String(30),
        default="aberta"
    )
    # aberta
    # paga
    # atrasada
    # negociando
    # cancelada

    observacoes = db.Column(
        db.Text
    )

    # Datas
    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relacionamentos
    conta = db.relationship(
        "Conta",
        backref="parcelas"
    )

    locacao = db.relationship(
        "Locacao",
        backref="parcelas"
    )

    @property
    def atrasada(self):
        if self.status == "paga":
            return False

        return self.vencimento < datetime.today().date()

    @property
    def dias_atraso(self):
        if not self.atrasada:
            return 0

        return (
            datetime.today().date() - self.vencimento
        ).days

    @property
    def saldo(self):
        return (
            (self.valor or 0)
            + (self.juros or 0)
            + (self.multa or 0)
            - (self.desconto or 0)
            - (self.valor_recebido or 0)
        )

    @property
    def quitada(self):
        return self.status == "paga"

    def __repr__(self):
        return f"Parcela {self.numero}"