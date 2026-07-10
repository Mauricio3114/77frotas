from datetime import date

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.models.parcela import Parcela


parcelas_bp = Blueprint(
    "parcelas",
    __name__,
    url_prefix="/parcelas"
)


@parcelas_bp.route("/")
@login_required
def listar():

    conta_id = current_user.conta_id
    hoje = date.today()

    status = request.args.get("status", "")

    query = Parcela.query.filter_by(
        conta_id=conta_id
    )

    if status == "pagas":

        query = query.filter(
            Parcela.status == "paga"
        )

    elif status == "atrasadas":

        query = query.filter(
            Parcela.status != "paga",
            Parcela.vencimento < hoje
        )

    elif status == "abertas":

        query = query.filter(
            Parcela.status != "paga"
        )

    parcelas = query.order_by(
        Parcela.vencimento.asc()
    ).all()

    total_aberto = sum(
        float(p.valor or 0)
        for p in parcelas
        if p.status != "paga"
    )

    total_pago = sum(
        float(p.valor_recebido or 0)
        for p in parcelas
        if p.status == "paga"
    )

    atrasadas = [
        p for p in parcelas
        if p.status != "paga" and p.vencimento < hoje
    ]

    print("Qtd parcelas:", len(parcelas))
    print("Primeira:", parcelas[0] if parcelas else None)

    return render_template(
        "parcelas/listar.html",
        parcelas=parcelas,
        hoje=hoje,
        total_aberto=total_aberto,
        total_pago=total_pago,
        total_atrasadas=len(atrasadas),
        status=status
    )