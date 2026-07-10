from app import db


class Modelo(db.Model):
    __tablename__ = "modelos"

    id = db.Column(db.Integer, primary_key=True)

    # Marca
    marca_id = db.Column(
        db.Integer,
        db.ForeignKey("marcas.id"),
        nullable=False
    )

    # Nome do modelo
    nome = db.Column(
        db.String(120),
        nullable=False
    )

    # Classificação
    categoria = db.Column(db.String(50))
    tipo_veiculo = db.Column(db.String(50))

    # Mecânica
    tipo_motorizacao = db.Column(db.String(30))
    combustivel_padrao = db.Column(db.String(30))
    cambio = db.Column(db.String(30))

    # Dimensões
    portas = db.Column(db.Integer)
    lugares = db.Column(db.Integer)

    # Elétricos / Híbridos
    capacidade_bateria = db.Column(db.Integer)
    autonomia_km = db.Column(db.Integer)
    tipo_conector = db.Column(db.String(30))
    potencia_recarga_kw = db.Column(db.Integer)

    # Caminhões / Utilitários
    pbt = db.Column(db.Numeric(10, 2))
    capacidade_carga = db.Column(db.Numeric(10, 2))
    quantidade_eixos = db.Column(db.Integer)
    tracao = db.Column(db.String(30))

    # Ônibus
    capacidade_passageiros = db.Column(db.Integer)

    # Situação
    ativo = db.Column(
        db.Boolean,
        default=True
    )

    def __repr__(self):
        return self.nome