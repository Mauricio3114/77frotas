from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from datetime import datetime

from flask_login import login_required, current_user
from sqlalchemy import or_

from app import db

from app.models.cliente import Cliente
from app.models.locacao import Locacao

from app.utils.pdf import gerar_pdf


clientes_bp = Blueprint(
    "clientes",
    __name__,
    url_prefix="/clientes"
)


@clientes_bp.route("/")
@login_required
def listar():

    busca = request.args.get("busca", "").strip()

    clientes = Cliente.query.filter(
        Cliente.conta_id == current_user.conta_id
    )

    if busca:

        clientes = clientes.filter(

            or_(

                Cliente.nome.ilike(f"%{busca}%"),

                Cliente.cpf.ilike(f"%{busca}%"),

                Cliente.telefone.ilike(f"%{busca}%"),

                Cliente.whatsapp.ilike(f"%{busca}%"),

                Cliente.email.ilike(f"%{busca}%")

            )

        )

    clientes = clientes.order_by(
        Cliente.nome.asc()
    ).all()

    return render_template(
        "clientes/listar.html",
        clientes=clientes
    )


@clientes_bp.route(
    "/novo",
    methods=["GET", "POST"]
)
@login_required
def novo():

    if request.method == "POST":

        data_nascimento = request.form.get(
            "data_nascimento"
        )

        validade_cnh = request.form.get(
            "validade_cnh"
        )

        if data_nascimento:

            data_nascimento = datetime.strptime(
                data_nascimento,
                "%Y-%m-%d"
            ).date()

        else:

            data_nascimento = None

        if validade_cnh:

            validade_cnh = datetime.strptime(
                validade_cnh,
                "%Y-%m-%d"
            ).date()

        else:

            validade_cnh = None

        cliente = Cliente(

            conta_id=current_user.conta_id,

            nome=request.form.get("nome"),

            cpf=request.form.get("cpf"),

            rg=request.form.get("rg"),

            data_nascimento=data_nascimento,

            numero_cnh=request.form.get("numero_cnh"),

            categoria_cnh=request.form.get("categoria_cnh"),

            validade_cnh=validade_cnh,

            telefone=request.form.get("telefone"),

            whatsapp=request.form.get("whatsapp"),

            email=request.form.get("email"),

            cep=request.form.get("cep"),

            endereco=request.form.get("endereco"),

            numero=request.form.get("numero"),

            bairro=request.form.get("bairro"),

            cidade=request.form.get("cidade"),

            estado=request.form.get("estado")

        )

        db.session.add(cliente)

        db.session.commit()

        flash(
            "Cliente cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for("clientes.listar")
        )

    return render_template(
        "clientes/novo.html"
    )


@clientes_bp.route("/<int:id>")
@login_required
def detalhes(id):

    cliente = Cliente.query.filter_by(
        id=id,
        conta_id=current_user.conta_id
    ).first_or_404()

    locacao_ativa = Locacao.query.filter_by(
        conta_id=current_user.conta_id,
        cliente_id=cliente.id,
        status="ativa"
    ).first()

    return render_template(
        "clientes/detalhes.html",
        cliente=cliente,
        locacao_ativa=locacao_ativa
    )


@clientes_bp.route("/<int:id>/editar")
@login_required
def editar(id):

    cliente = Cliente.query.filter_by(
        id=id,
        conta_id=current_user.conta_id
    ).first_or_404()

    return render_template(
        "clientes/editar.html",
        cliente=cliente
    )


@clientes_bp.route("/clientes/pdf")
@login_required
def clientes_pdf():

    clientes = Cliente.query.filter_by(
        conta_id=current_user.conta_id
    ).order_by(
        Cliente.nome.asc()
    ).all()

    linhas = []

    for cliente in clientes:

        linhas.append([
            cliente.nome,
            cliente.cpf or "-",
            cliente.telefone or "-"
        ])

    return gerar_pdf(

        titulo="Relatório de Clientes",

        cabecalho=[
            "Nome",
            "CPF",
            "Telefone"
        ],

        linhas=linhas,

        nome_arquivo="clientes.pdf"

    )


@clientes_bp.route("/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):

    cliente = Cliente.query.filter_by(
        id=id,
        conta_id=current_user.conta_id
    ).first_or_404()

    locacao_ativa = Locacao.query.filter_by(
        conta_id=current_user.conta_id,
        cliente_id=cliente.id,
        status="ativa"
    ).first()

    if locacao_ativa:

        flash(
            "Este cliente possui uma locação ativa e não pode ser excluído.",
            "warning"
        )

        return redirect(
            url_for("clientes.listar")
        )

    db.session.delete(cliente)

    db.session.commit()

    flash(
        "Cliente excluído com sucesso.",
        "success"
    )

    return redirect(
        url_for("clientes.listar")
    )