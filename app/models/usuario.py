from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    conta_id = db.Column(db.Integer, db.ForeignKey("contas.id"), nullable=True)

    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    perfil = db.Column(db.String(30), nullable=False, default="ADMIN")
    ativo = db.Column(db.Boolean, default=True)

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_master(self):
        return self.perfil == "MASTER"

    @property
    def is_admin(self):
        return self.perfil == "ADMIN"

    @property
    def is_cliente(self):
        return self.perfil == "CLIENTE"