from datetime import date

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.veiculo import Veiculo
from app.models.cliente import Cliente
from app.models.locacao import Locacao
from app.models.parcela import Parcela


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.perfil != "ADMIN":
        return "Acesso negado.", 403

    conta_id = current_user.conta_id
    hoje = date.today()

    primeiro_dia_mes = hoje.replace(day=1)

    if hoje.month == 12:
        primeiro_dia_proximo_mes = date(hoje.year + 1, 1, 1)
    else:
        primeiro_dia_proximo_mes = date(
            hoje.year,
            hoje.month + 1,
            1
        )

    total_clientes = Cliente.query.filter_by(
        conta_id=conta_id
    ).count()

    total_veiculos = Veiculo.query.filter_by(
        conta_id=conta_id,
        ativo=True
    ).count()

    veiculos_locados = Veiculo.query.filter_by(
        conta_id=conta_id,
        ativo=True,
        status="locado"
    ).count()

    veiculos_disponiveis = Veiculo.query.filter_by(
        conta_id=conta_id,
        ativo=True,
        status="disponivel"
    ).count()

    total_locacoes = Locacao.query.filter_by(
        conta_id=conta_id
    ).count()

    parcelas_receber_hoje = Parcela.query.filter(
        Parcela.conta_id == conta_id,
        Parcela.vencimento == hoje,
        Parcela.status != "paga"
    ).all()

    parcelas_atrasadas = Parcela.query.filter(
        Parcela.conta_id == conta_id,
        Parcela.vencimento < hoje,
        Parcela.status != "paga"
    ).all()

    parcelas_recebidas_hoje = Parcela.query.filter(
        Parcela.conta_id == conta_id,
        Parcela.data_pagamento == hoje,
        Parcela.status == "paga"
    ).all()

    parcelas_previsao_mes = Parcela.query.filter(
        Parcela.conta_id == conta_id,
        Parcela.status != "paga",
        Parcela.vencimento >= primeiro_dia_mes,
        Parcela.vencimento < primeiro_dia_proximo_mes
    ).all()

    veiculos_livres = Veiculo.query.filter_by(
        conta_id=conta_id,
        ativo=True,
        status="disponivel"
    ).limit(6).all()

    ultimas_locacoes = Locacao.query.filter_by(
        conta_id=conta_id
    ).order_by(
        Locacao.data_cadastro.desc()
    ).limit(6).all()

    ultimas_parcelas = Parcela.query.filter(
        Parcela.conta_id == conta_id,
        Parcela.status != "paga"
    ).order_by(
        Parcela.vencimento.asc()
    ).limit(8).all()

    receber_hoje = sum(
        float(parcela.valor or 0)
        for parcela in parcelas_receber_hoje
    )

    previsao_recebimentos = sum(
        float(parcela.valor or 0)
        for parcela in parcelas_previsao_mes
    )

    recebido_hoje = sum(
        float(parcela.valor_recebido or 0)
        for parcela in parcelas_recebidas_hoje
    )

    valor_atrasado = sum(
        float(parcela.valor or 0)
        for parcela in parcelas_atrasadas
    )

    return render_template(
        "dashboard/index.html",
        total_clientes=total_clientes,
        total_veiculos=total_veiculos,
        total_locacoes=total_locacoes,
        veiculos_locados=veiculos_locados,
        veiculos_disponiveis=veiculos_disponiveis,
        receber_hoje=receber_hoje,
        receber_mes=previsao_recebimentos,
        recebido_hoje=recebido_hoje,
        parcelas_atrasadas=len(parcelas_atrasadas),
        valor_atrasado=valor_atrasado,
        custos_mes=0,
        vencimentos_hoje=parcelas_receber_hoje,
        atrasadas=parcelas_atrasadas,
        veiculos_livres=veiculos_livres,
        ultimas_locacoes=ultimas_locacoes,
        ultimas_parcelas=ultimas_parcelas,
        negociacoes=[]
    )