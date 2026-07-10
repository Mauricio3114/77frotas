from getpass import getpass

from app import create_app, db
from app.models.usuario import Usuario


app = create_app()

with app.app_context():
    print("\n=== Criar usuário MASTER | 77 Frotas ===\n")

    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()
    senha = getpass("Senha: ").strip()

    if not nome or not email or not senha:
        print("Nome, e-mail e senha são obrigatórios.")
        exit()

    existe = Usuario.query.filter_by(email=email).first()

    if existe:
        print("Já existe um usuário com esse e-mail.")
        exit()

    usuario = Usuario(
        nome=nome,
        email=email,
        perfil="MASTER",
        ativo=True,
        conta_id=None
    )

    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    print("\nMASTER criado com sucesso!")
    print(f"E-mail: {email}")