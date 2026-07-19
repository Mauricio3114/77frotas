import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

import app.cloudinary_config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///77frotas.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.conta import Conta
    from app.models.usuario import Usuario
    from app.models.marca import Marca
    from app.models.modelo import Modelo
    from app.models.veiculo import Veiculo
    from app.models.cliente import Cliente
    from app.models.locacao import Locacao
    from app.models.parcela import Parcela
    from app.models.pagamento import Pagamento
    from app.models.despesa import Despesa
    from app.models.negociacao import Negociacao
    from app.models.solicitacao_negociacao import SolicitacaoNegociacao

    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para continuar."

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.master import master_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.clientes import clientes_bp
    from app.routes.veiculos import veiculos_bp
    from app.routes.locacoes import locacoes_bp
    from app.routes.despesas import despesas_bp
    from app.routes.parcelas import parcelas_bp
    from app.routes.recebimentos import recebimentos_bp
    from app.routes.portal import portal_bp
    from app.routes.negociacoes import negociacoes_bp
    from app.routes.configuracoes import configuracoes_bp
    from app.routes.analysis_center import analysis_center_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(master_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(veiculos_bp)
    app.register_blueprint(locacoes_bp)
    app.register_blueprint(despesas_bp)
    app.register_blueprint(parcelas_bp)
    app.register_blueprint(recebimentos_bp)
    app.register_blueprint(portal_bp)
    app.register_blueprint(negociacoes_bp)
    app.register_blueprint(configuracoes_bp)
    app.register_blueprint(analysis_center_bp)

    with app.app_context():
        from app.bootstrap import bootstrap
        bootstrap()

    @app.template_filter("moeda")
    def moeda(valor):
        try:
            valor = float(valor or 0)

            numero = f"{valor:,.2f}"

            numero = numero.replace(",", "X")
            numero = numero.replace(".", ",")
            numero = numero.replace("X", ".")

            return f"R$ {numero}"

        except (TypeError, ValueError):
            return "R$ 0,00"
            print("✅ Filtro moeda registrado")


    @app.template_filter("data_br")
    def data_br(valor):
        if not valor:
            return "-"

        try:
            return valor.strftime("%d/%m/%Y")

        except AttributeError:
            return str(valor)

        print("✅ Filtro data_br registrado")

        print("Filtros disponíveis:")
        print(app.jinja_env.filters.keys())

    return app