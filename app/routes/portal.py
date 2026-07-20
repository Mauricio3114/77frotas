from datetime import datetime,date

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.locacao import Locacao
from app.models.parcela import Parcela
from app.models.pagamento import Pagamento

from cloudinary.uploader import upload
from werkzeug.utils import secure_filename
from app.models.pagamento import Pagamento
from app import db


portal_bp = Blueprint(
    "portal",
    __name__,
    url_prefix="/portal"
)


def cliente_logado():
    cliente_id = session.get("portal_cliente_id")

    if not cliente_id:
        return None

    return Cliente.query.get(cliente_id)


def portal_login_required(func):
    def wrapper(*args, **kwargs):
        cliente = cliente_logado()

        if not cliente:
            return redirect(url_for("portal.login"))

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__

    return wrapper


@portal_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        cpf = (
            request.form.get("cpf") or ""
        ).replace(".", "").replace("-", "").replace(" ", "")

        senha = (
            request.form.get("senha") or ""
        ).strip()

        cliente = None

        clientes = Cliente.query.filter_by(
            ativo=True
        ).all()

        for c in clientes:

            cpf_cliente = (
                c.cpf or ""
            ).replace(".", "").replace("-", "").replace(" ", "")

            if cpf_cliente == cpf:

                cliente = c
                break

        if not cliente:
            flash(
                "CPF não encontrado no Portal 77 Frotas.",
                "danger"
            )

            return redirect(url_for("portal.login"))

        if not cliente.ativo:

            flash(
                "Seu cadastro está inativo. Entre em contato com sua locadora.",
                "warning"
            )

            return redirect(
                url_for("portal.login")
            )

        data_nascimento = cliente.data_nascimento

        if hasattr(data_nascimento, "strftime"):
            senha_correta = data_nascimento.strftime("%d%m%Y")
        else:
            senha_correta = str(data_nascimento).replace("/", "").replace("-", "")

        if senha != senha_correta:
            flash(
                "CPF ou data de nascimento inválidos.",
                "danger"
            )

            return redirect(url_for("portal.login"))

        session["portal_cliente_id"] = cliente.id

        return redirect(
            url_for("portal.instalar")
        )

    return render_template("portal/login.html")


@portal_bp.route("/sair")
def sair():

    session.pop("portal_cliente_id", None)

    return redirect(url_for("portal.login"))


@portal_bp.route("/")
@portal_login_required
def home():

    cliente = cliente_logado()

    return render_template(
        "portal/home.html",
        cliente=cliente
    )


@portal_bp.route("/veiculos")
@portal_login_required
def veiculos():

    cliente = cliente_logado()

    veiculos = (
        Veiculo.query
        .join(Conta)
        .filter(
            Veiculo.status == "disponivel",
            Veiculo.ativo == True,
            Conta.status == "ativo"
        )
        .order_by(Veiculo.id.desc())
        .all()
    )

    return render_template(
        "portal/veiculos.html",
        cliente=cliente,
        veiculos=veiculos
    )


@portal_bp.route("/meu-veiculo")
@portal_login_required
def meu_veiculo():

    cliente = cliente_logado()

    locacao = (
        Locacao.query.filter_by(
            cliente_id=cliente.id
        )
        .order_by(Locacao.id.desc())
        .first()
    )

    return render_template(
        "portal/meu_veiculo.html",
        cliente=cliente,
        locacao=locacao
    )


@portal_bp.route("/parcelas")
@portal_login_required
def parcelas():

    cliente = cliente_logado()

    locacoes = Locacao.query.filter_by(
        cliente_id=cliente.id
    ).all()

    locacoes_ids = [
        l.id for l in locacoes
    ]

    parcelas = Parcela.query.filter(
        Parcela.locacao_id.in_(locacoes_ids)
    ).order_by(
        Parcela.vencimento.asc()
    ).all() if locacoes_ids else []

    return render_template(
        "portal/parcelas.html",
        cliente=cliente,
        parcelas=parcelas,
        hoje=date.today()
    )


@portal_bp.route("/pagamentos")
@portal_login_required
def pagamentos():

    cliente = cliente_logado()

    locacoes = Locacao.query.filter_by(
        cliente_id=cliente.id
    ).all()

    locacoes_ids = [
        l.id for l in locacoes
    ]

    parcelas = Parcela.query.filter(
        Parcela.locacao_id.in_(locacoes_ids)
    ).all() if locacoes_ids else []

    parcelas_ids = [
        p.id for p in parcelas
    ]

    pagamentos = Pagamento.query.filter(
        Pagamento.parcela_id.in_(parcelas_ids)
    ).order_by(
        Pagamento.data_pagamento.desc()
    ).all() if parcelas_ids else []

    return render_template(
        "portal/pagamentos.html",
        cliente=cliente,
        pagamentos=pagamentos
    )


@portal_bp.route("/meu-cadastro")
@portal_login_required
def meu_cadastro():

    cliente = cliente_logado()

    return render_template(
        "portal/meu_cadastro.html",
        cliente=cliente
    )


@portal_bp.route("/negociacao/<int:parcela_id>", methods=["GET", "POST"])
@portal_login_required
def solicitar_negociacao(parcela_id):

    from app import db
    from app.models.solicitacao_negociacao import SolicitacaoNegociacao

    cliente = cliente_logado()

    parcela = Parcela.query.get_or_404(parcela_id)


    if request.method == "POST":

        solicitacao = SolicitacaoNegociacao(

            conta_id=parcela.conta_id,

            parcela_id=parcela.id,

            cliente_id=cliente.id,

            valor_proposto=request.form.get("valor_proposto") or 0,

            nova_data=datetime.strptime(
                request.form.get("nova_data"),
                "%Y-%m-%d"
            ).date(),

            motivo=request.form.get("motivo"),

            status="pendente"

        )

        db.session.add(solicitacao)

        db.session.commit()

        flash(
            "Sua solicitação foi enviada para análise da locadora.",
            "success"
        )

        return redirect(
            url_for("portal.parcelas")
        )

    return render_template(
        "portal/solicitar_negociacao.html",
        cliente=cliente,
        parcela=parcela
    )


@portal_bp.route("/instalar")
@portal_login_required
def instalar():

    cliente = cliente_logado()

    return render_template(
        "portal/instalar.html",
        cliente=cliente
    )


@portal_bp.route(
    "/pagamento/<int:parcela_id>",
    methods=["GET", "POST"]
)

@portal_login_required
def pagamento_pix(parcela_id):

    cliente = cliente_logado()

    parcela = Parcela.query.get_or_404(parcela_id)

    pagamento_existente = Pagamento.query.filter_by(
        parcela_id=parcela.id
    ).filter(
        Pagamento.webhook_recebido == False
    ).first()

    if pagamento_existente:
        flash(
            "Já existe um pagamento aguardando confirmação para esta parcela.",
            "warning"
        )

        return redirect(
            url_for("portal.parcelas")
        )

    if request.method == "POST":

        url_comprovante = None

        arquivo = request.files.get("comprovante")

        if arquivo and arquivo.filename:

            resultado = upload(
                arquivo,
                folder=f"77frotas/comprovantes/conta_{parcela.conta_id}",
                resource_type="auto"
            )

            url_comprovante = resultado["secure_url"]

        pagamento = Pagamento(

            conta_id=parcela.conta_id,

            parcela_id=parcela.id,

            valor=parcela.valor,

            forma_pagamento="pix",

            gateway="Manual",

            webhook_recebido=False,

            comprovante=url_comprovante,

            observacoes="Pagamento informado pelo cliente. Aguardando confirmação da locadora."

        )

        db.session.add(pagamento)

        db.session.commit()

        flash(
            "Pagamento informado com sucesso. Aguarde a confirmação da locadora.",
            "success"
        )

        return redirect(
            url_for("portal.pagamento_enviado")
        )

    return render_template(
        "portal/pagamento_pix.html",
        cliente=cliente,
        parcela=parcela,
        conta=parcela.conta
    )


@portal_bp.route("/pagamento-enviado")
@portal_login_required
def pagamento_enviado():

    cliente = cliente_logado()

    return render_template(
        "portal/pagamento_enviado.html",
        cliente=cliente
    )