from datetime import datetime
from app import db


class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)

    # Conta
    conta_id = db.Column(
        db.Integer,
        db.ForeignKey("contas.id"),
        nullable=False
    )

    # Parcela
    parcela_id = db.Column(
        db.Integer,
        db.ForeignKey("parcelas.id"),
        nullable=False
    )

    valor = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    data_pagamento = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    forma_pagamento = db.Column(
        db.String(30)
    )
    # pix
    # dinheiro
    # cartao
    # transferencia
    # mercado_pago
    # efi

    gateway = db.Column(
        db.String(30)
    )
    # Mercado Pago
    # Efí
    # Manual

    codigo_transacao = db.Column(
        db.String(200)
    )

    webhook_recebido = db.Column(
        db.Boolean,
        default=False
    )

    comprovante = db.Column(
        db.String(255)
    )

    observacoes = db.Column(db.Text)

    conta = db.relationship(
        "Conta",
        backref="pagamentos"
    )

    parcela = db.relationship(
        "Parcela",
        backref="pagamentos"
    )

    def __repr__(self):
        return f"Pagamento #{self.id}"