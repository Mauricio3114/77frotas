from datetime import datetime
from app import db


class Conta(db.Model):
    __tablename__ = "contas"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(180), nullable=False)
    cpf_cnpj = db.Column(db.String(30))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(150))

    logo = db.Column(db.String(255))
    cor_primaria = db.Column(db.String(20), default="#0f172a")

    chave_pix = db.Column(db.String(255))

    # PIX
    tipo_chave_pix = db.Column(
        db.String(30),
        default="cpf"
    )
    # cpf
    # cnpj
    # celular
    # email
    # aleatoria

    favorecido_pix = db.Column(
        db.String(150)
    )

    banco_pix = db.Column(
        db.String(100)
    )

    plano = db.Column(db.String(50), default="basico")
    status = db.Column(db.String(30), default="ativo")

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_acesso = db.Column(db.DateTime)

    usuarios = db.relationship("Usuario", backref="conta", lazy=True)