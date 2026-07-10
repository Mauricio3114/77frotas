from sqlalchemy import inspect

from app import db
from app.models.usuario import Usuario


def bootstrap():

    inspector = inspect(db.engine)

    # Aguarda as migrations criarem as tabelas
    if "usuarios" not in inspector.get_table_names():
        return

    EMAIL = "master@77frotas.com"
    SENHA = "123456"

    usuario = Usuario.query.filter_by(
        email=EMAIL
    ).first()

    if usuario:
        return

    usuario = Usuario(
        nome="MASTER",
        email=EMAIL,
        perfil="MASTER",
        ativo=True,
        conta_id=None
    )

    usuario.set_senha(SENHA)

    db.session.add(usuario)
    db.session.commit()

    print("✅ Usuário MASTER criado automaticamente.")