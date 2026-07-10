from datetime import datetime
from app import db


class Veiculo(db.Model):
    __tablename__ = "veiculos"

    id = db.Column(db.Integer, primary_key=True)

    # Conta (Locadora)
    conta_id = db.Column(
        db.Integer,
        db.ForeignKey("contas.id"),
        nullable=False
    )

    # Dados Básicos
    marca = db.Column(
        db.String(100),
        nullable=False
    )

    modelo = db.Column(
        db.String(120),
        nullable=False
    )

    categoria = db.Column(db.String(50))

    placa = db.Column(
        db.String(20),
        nullable=False
    )

    renavam = db.Column(db.String(50))

    chassi = db.Column(db.String(80))

    ano_fabricacao = db.Column(db.String(4))
    ano_modelo = db.Column(db.String(4))

    cor = db.Column(db.String(50))
    combustivel = db.Column(db.String(50))

    cambio = db.Column(db.String(30))
    portas = db.Column(db.Integer)
    lugares = db.Column(db.Integer)

    # Controle
    km_atual = db.Column(
        db.Integer,
        default=0
    )

    # Comercial
    valor_diaria = db.Column(
        db.Numeric(10, 2),
        default=0
    )

    valor_fipe = db.Column(
        db.Numeric(12, 2),
        default=0
    )

    proprietario = db.Column(
        db.String(30),
        default="proprio"
    )

    # Arquivos
    foto_principal = db.Column(db.String(255))

    # Situação
    status = db.Column(
        db.String(30),
        default="disponivel"
    )

    ativo = db.Column(
        db.Boolean,
        default=True
    )

    # Observações
    observacoes = db.Column(db.Text)

    # Datas
    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relacionamento
    conta = db.relationship(
        "Conta",
        backref="veiculos"
    )

    @property
    def valor_semanal(self):
        return (self.valor_diaria or 0) * 7

    @property
    def valor_mensal(self):
        return (self.valor_diaria or 0) * 30

    @property
    def disponivel(self):
        return self.status == "disponivel"