from datetime import datetime
from app import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    # Conta
    conta_id = db.Column(
        db.Integer,
        db.ForeignKey("contas.id"),
        nullable=False
    )

    # Dados pessoais
    nome = db.Column(
        db.String(150),
        nullable=False
    )

    cpf = db.Column(db.String(20))
    rg = db.Column(db.String(20))

    data_nascimento = db.Column(db.Date)

    # CNH
    numero_cnh = db.Column(db.String(30))
    categoria_cnh = db.Column(db.String(10))
    validade_cnh = db.Column(db.Date)

    # Contato
    telefone = db.Column(db.String(30))
    whatsapp = db.Column(db.String(30))
    email = db.Column(db.String(150))

    # Endereço
    cep = db.Column(db.String(15))
    endereco = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))

    # Financeiro
    chave_pix = db.Column(db.String(150))

    # Documentos
    foto_cliente = db.Column(db.String(255))
    foto_cnh = db.Column(db.String(255))
    comprovante_residencia = db.Column(db.String(255))

    # Situação
    status = db.Column(
        db.String(30),
        default="ativo"
    )
    # ativo
    # inadimplente
    # bloqueado

    observacoes = db.Column(db.Text)

    data_cadastro = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    conta = db.relationship(
        "Conta",
        backref="clientes"
    )

    @property
    def nome_resumido(self):
        nomes = self.nome.split()

        if len(nomes) <= 2:
            return self.nome

        return f"{nomes[0]} {nomes[-1]}"

    @property
    def possui_locacao(self):
        return len(self.locacoes) > 0

    def __repr__(self):
        return self.nome