from datetime import datetime

from app import db


class SolicitacaoNegociacao(db.Model):
    __tablename__ = "solicitacoes_negociacao"

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

    parcela_id = db.Column(
        db.Integer,
        db.ForeignKey("parcelas.id"),
        nullable=False
    )

    valor_proposto = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    nova_data = db.Column(
        db.Date,
        nullable=False
    )

    motivo = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="pendente"
    )
    # pendente
    # aprovada
    # recusada

    observacao_admin = db.Column(
        db.Text
    )

    data_solicitacao = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    data_resposta = db.Column(
        db.DateTime
    )

    cliente = db.relationship(
        "Cliente",
        backref="solicitacoes_negociacao"
    )

    conta = db.relationship(
        "Conta",
        backref="solicitacoes_negociacao"
    )

    parcela = db.relationship(
        "Parcela",
        backref="solicitacoes_negociacao"
    )

    def __repr__(self):
        return f"<Solicitação {self.id}>"