from sqlalchemy import inspect

from app import db
from app.models.usuario import Usuario


def bootstrap():

    inspector = inspect(db.engine)

    # Aguarda o banco ser criado pelas migrations
    if "usuarios" not in inspector.get_table_names():
        return

    EMAIL = "master@77frotas.com"
    SENHA = "123456"

    master = Usuario.query.filter_by(
        email=EMAIL
    ).first()

    # Já existe
    if master:
        return

    master = Usuario(
        nome="Master",
        email=EMAIL,
        perfil="MASTER",
        ativo=True,
        conta_id=None
    )

    master.set_senha(SENHA)

    db.session.add(master)
    db.session.commit()

    print("✅ Master criado automaticamente.")