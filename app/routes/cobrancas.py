from datetime import date, timedelta

from flask import (
    Blueprint,
    render_template,
    request
)

from flask_login import (
    login_required,
    current_user
)

from app.models.parcela import Parcela


cobrancas_bp = Blueprint(
    "cobrancas",
    __name__,
    url_prefix="/cobrancas"
)


@cobrancas_bp.route("/")
@login_required
def listar():

    hoje = date.today()

    filtro = request.args.get(
        "filtro",
        "todas"
    )

    query = Parcela.query.filter(
        Parcela.conta_id == current_user.conta_id,
        Parcela.status != "paga"
    )

    if filtro == "vencidas":

        query = query.filter(
            Parcela.vencimento < hoje
        )

    elif filtro == "hoje":

        query = query.filter(
            Parcela.vencimento == hoje
        )

    elif filtro == "7dias":

        query = query.filter(
            Parcela.vencimento >= hoje,
            Parcela.vencimento <= hoje + timedelta(days=7)
        )

    elif filtro == "30dias":

        query = query.filter(
            Parcela.vencimento >= hoje,
            Parcela.vencimento <= hoje + timedelta(days=30)
        )

    parcelas = query.order_by(
        Parcela.vencimento.asc()
    ).all()

    total_aberto = sum(
        float(p.valor or 0)
        for p in parcelas
    )

    vencidas = sum(
        1
        for p in parcelas
        if p.vencimento < hoje
    )

    vencem_hoje = sum(
        1
        for p in parcelas
        if p.vencimento == hoje
    )

    proximos_7 = sum(
        1
        for p in parcelas
        if hoje <= p.vencimento <= hoje + timedelta(days=7)
    )

    return render_template(

        "cobrancas/listar.html",

        parcelas=parcelas,

        hoje=hoje,

        filtro=filtro,

        total_aberto=total_aberto,

        vencidas=vencidas,

        vencem_hoje=vencem_hoje,

        proximos_7=proximos_7

    )