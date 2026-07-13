from decimal import Decimal

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.veiculo import Veiculo
from app.models.marca import Marca
from app.models.modelo import Modelo

from flask import jsonify


veiculos_bp = Blueprint("veiculos", __name__, url_prefix="/veiculos")


@veiculos_bp.route("/")
@login_required
def listar():
    veiculos = Veiculo.query.filter_by(
        conta_id=current_user.conta_id
    ).order_by(Veiculo.id.desc()).all()

    return render_template("veiculos/listar.html", veiculos=veiculos)


@veiculos_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():

    marcas = Marca.query.filter_by(
        ativo=True
    ).order_by(
        Marca.nome
    ).all()

    modelos = Modelo.query.filter_by(
        ativo=True
    ).order_by(
        Modelo.nome
    ).all()

    if request.method == "POST":

        placa = request.form.get(
            "placa",
            ""
        ).strip().upper()

        if not placa:

            flash(
                "Informe a placa do veículo.",
                "warning"
            )

            return redirect(
                url_for("veiculos.novo")
            )

        existe = Veiculo.query.filter_by(
            conta_id=current_user.conta_id,
            placa=placa
        ).first()

        if existe:

            flash(
                "Já existe um veículo com essa placa.",
                "danger"
            )

            return redirect(
                url_for("veiculos.novo")
            )

        # ===================================
        # CONVERTE O ID DA MARCA PARA O NOME
        # ===================================

        marca_id = request.form.get("marca")

        marca_nome = ""

        if marca_id:

            marca = Marca.query.get(
                int(marca_id)
            )

            if marca:

                marca_nome = marca.nome

        # ===================================
        # CONVERTE O ID DO MODELO PARA O NOME
        # ===================================

        modelo_id = request.form.get("modelo")

        modelo_nome = ""

        if modelo_id:

            modelo = Modelo.query.get(
                int(modelo_id)
            )

            if modelo:

                modelo_nome = modelo.nome

        veiculo = Veiculo(

            conta_id=current_user.conta_id,

            marca=marca_nome,

            modelo=modelo_nome,

            categoria=request.form.get(
                "categoria",
                ""
            ).strip(),

            placa=placa,

            renavam=request.form.get(
                "renavam",
                ""
            ).strip(),

            chassi=request.form.get(
                "chassi",
                ""
            ).strip(),

            ano_fabricacao=request.form.get(
                "ano_fabricacao",
                ""
            ).strip(),

            ano_modelo=request.form.get(
                "ano_modelo",
                ""
            ).strip(),

            cor=request.form.get(
                "cor",
                ""
            ).strip(),

            combustivel=request.form.get(
                "combustivel",
                ""
            ).strip(),

            cambio=request.form.get(
                "cambio",
                ""
            ).strip(),

            portas=int(
                request.form.get("portas") or 0
            ),

            lugares=int(
                request.form.get("lugares") or 0
            ),

            km_atual=int(
                request.form.get("km_atual") or 0
            ),

            valor_diaria=Decimal(
                request.form.get("valor_diaria") or 0
            ),

            status=request.form.get(
                "status",
                "disponivel"
            ),

            observacoes=request.form.get(
                "observacoes",
                ""
            ).strip()

        )

        db.session.add(veiculo)

        db.session.commit()

        flash(
            "Veículo cadastrado com sucesso.",
            "success"
        )

        return redirect(
            url_for(
                "veiculos.detalhes",
                id=veiculo.id
            )
        )

    return render_template(
        "veiculos/novo.html",
        marcas=marcas,
        modelos=modelos
    )


@veiculos_bp.route("/<int:id>")
@login_required
def detalhes(id):
    veiculo = Veiculo.query.filter_by(
        id=id,
        conta_id=current_user.conta_id
    ).first_or_404()

    return render_template("veiculos/detalhes.html", veiculo=veiculo)


@veiculos_bp.route("/<int:id>/editar")
@login_required
def editar(id):
    veiculo = Veiculo.query.filter_by(
        id=id,
        conta_id=current_user.conta_id
    ).first_or_404()

    marcas = Marca.query.filter_by(ativo=True).order_by(Marca.nome).all()
    modelos = Modelo.query.filter_by(ativo=True).order_by(Modelo.nome).all()

    return render_template(
        "veiculos/editar.html",
        veiculo=veiculo,
        marcas=marcas,
        modelos=modelos
    )


@veiculos_bp.route("/modelos/<int:marca_id>")
@login_required
def modelos(marca_id):

    modelos = Modelo.query.filter_by(
        marca_id=marca_id,
        ativo=True
    ).order_by(
        Modelo.nome
    ).all()

    return jsonify([
        {
            "id": modelo.id,
            "nome": modelo.nome
        }
        for modelo in modelos
    ])


@veiculos_bp.route("/<int:id>/excluir", methods=["POST"])
@login_required
def excluir(id):

    veiculo = Veiculo.query.filter_by(
        id=id,
        conta_id=current_user.conta_id
    ).first_or_404()

    if veiculo.locacoes:

        flash(
            "Não é possível excluir um veículo que possui locações.",
            "warning"
        )

        return redirect(
            url_for("veiculos.listar")
        )

    db.session.delete(veiculo)
    db.session.commit()

    flash(
        "Veículo excluído com sucesso.",
        "success"
    )

    return redirect(
        url_for("veiculos.listar")
    )
