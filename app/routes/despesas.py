from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.despesa import Despesa
from app.models.veiculo import Veiculo


despesas_bp = Blueprint("despesas", __name__)


@despesas_bp.route("/despesas")
@login_required
def listar_despesas():

    despesas = Despesa.query.filter_by(
        conta_id=current_user.conta_id
    ).order_by(
        Despesa.data.desc()
    ).all()

    return render_template(
        "despesas/listar.html",
        despesas=despesas
    )


@despesas_bp.route(
    "/despesas/nova",
    methods=["GET", "POST"]
)
@login_required
def nova_despesa():

    if request.method == "POST":

        despesa = Despesa(

            conta_id=current_user.conta_id,

            veiculo_id=request.form.get("veiculo_id"),

            tipo=request.form.get("tipo"),

            valor=request.form.get("valor"),

            data=request.form.get("data"),

            observacoes=request.form.get("observacoes")

        )

        db.session.add(despesa)
        db.session.commit()

        flash(
            "Despesa cadastrada com sucesso.",
            "success"
        )

        return redirect(
            url_for("despesas.listar_despesas")
        )

    veiculos = Veiculo.query.filter_by(
        conta_id=current_user.conta_id
    ).all()

    return render_template(
        "despesas/nova.html",
        veiculos=veiculos
    )


@despesas_bp.route(
    "/despesas/<int:id>/editar",
    methods=["GET", "POST"]
)
@login_required
def editar_despesa(id):

    despesa = Despesa.query.filter_by(
        id=id,
        conta_id=current_user.conta_id
    ).first_or_404()

    if request.method == "POST":

        despesa.veiculo_id = request.form.get("veiculo_id")
        despesa.tipo = request.form.get("tipo")
        despesa.valor = request.form.get("valor")
        despesa.data = request.form.get("data")
        despesa.observacoes = request.form.get("observacoes")

        db.session.commit()

        flash(
            "Despesa atualizada.",
            "success"
        )

        return redirect(
            url_for("despesas.listar_despesas")
        )

    veiculos = Veiculo.query.filter_by(
        conta_id=current_user.conta_id
    ).all()

    return render_template(
        "despesas/editar.html",
        despesa=despesa,
        veiculos=veiculos
    )


@despesas_bp.route(
    "/despesas/<int:id>/excluir",
    methods=["POST"]
)
@login_required
def excluir_despesa(id):

    despesa = Despesa.query.filter_by(
        id=id,
        conta_id=current_user.conta_id
    ).first_or_404()

    db.session.delete(despesa)
    db.session.commit()

    flash(
        "Despesa excluída.",
        "success"
    )

    return redirect(
        url_for("despesas.listar_despesas")
    )