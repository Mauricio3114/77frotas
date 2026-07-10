from sqlalchemy import inspect

from app import db
from app.models.conta import Conta
from app.models.usuario import Usuario


def bootstrap():

    inspector = inspect(db.engine)

    # Se as tabelas ainda não existem,
    # não faz nada.
    if "usuarios" not in inspector.get_table_names():
        return

    EMAIL = "master@77frotas.com"
    SENHA = "123456"

    #
    # Conta Master
    #

    conta = Conta.query.filter_by(
        email=EMAIL
    ).first()

    if not conta:

        conta = Conta(

            nome="77 Frotas",

            cpf_cnpj="00000000000000",

            telefone="",

            email=EMAIL,

            plano="basico",

            status="ativo",

            cor_primaria="#0f172a"

        )

        db.session.add(conta)
        db.session.commit()

        print("✔ Conta MASTER criada.")

    #
    # Usuário Master
    #

    usuario = Usuario.query.filter_by(
        email=EMAIL
    ).first()

    if not usuario:

        usuario = Usuario(

            nome="MASTER",

            email=EMAIL,

            perfil="MASTER",

            ativo=True,

            conta_id=conta.id

        )

        usuario.set_senha(SENHA)

        db.session.add(usuario)
        db.session.commit()

        print("✔ Usuário MASTER criado.")