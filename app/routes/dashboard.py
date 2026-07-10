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

    total_clientes = Cliente.query.filter_by(conta_id=conta_id).count()

    veiculos_locados = Veiculo.query.filter_by(
        conta_id=conta_id,
        status="locado"
    ).count()

    veiculos_disponiveis = Veiculo.query.filter_by(
        conta_id=conta_id,
        status="disponivel"
    ).count()

    receber_hoje = Parcela.query.filter(
        Parcela.conta_id == conta_id,
        Parcela.vencimento == hoje,
        Parcela.status != "paga"
    ).all()

    parcelas_atrasadas = Parcela.query.filter(
        Parcela.conta_id == conta_id,
        Parcela.vencimento < hoje,
        Parcela.status != "paga"
    ).all()

    recebido_hoje = Parcela.query.filter(
        Parcela.conta_id == conta_id,
        Parcela.data_pagamento == hoje,
        Parcela.status == "paga"
    ).all()

    veiculos_livres = Veiculo.query.filter_by(
        conta_id=conta_id,
        status="disponivel"
    ).limit(6).all()

    ultimas_locacoes = Locacao.query.filter_by(
        conta_id=conta_id
    ).order_by(
        Locacao.data_cadastro.desc()
    ).limit(6).all()

    total_veiculos = Veiculo.query.filter_by(
    conta_id=conta_id
    ).count()

    total_locacoes = Locacao.query.filter_by(
        conta_id=conta_id
    ).count()

    receber_mes = sum(
        float(p.valor)
        for p in Parcela.query.filter(
            Parcela.conta_id == conta_id,
            Parcela.status != "paga"
        ).all()
    )

    ultimas_parcelas = Parcela.query.filter_by(
        conta_id=conta_id
    ).order_by(
        Parcela.vencimento.asc()
    ).limit(8).all()

    return render_template(

        "dashboard/index.html",

        total_clientes=total_clientes,

        total_veiculos=total_veiculos,

        total_locacoes=total_locacoes,

        veiculos_locados=veiculos_locados,

        veiculos_disponiveis=veiculos_disponiveis,

        receber_hoje=sum(float(p.valor) for p in receber_hoje),

        receber_mes=receber_mes,

        recebido_hoje=sum(float(p.valor_recebido or 0) for p in recebido_hoje),

        parcelas_atrasadas=len(parcelas_atrasadas),

        valor_atrasado=sum(float(p.valor) for p in parcelas_atrasadas),

        custos_mes=0,

        vencimentos_hoje=receber_hoje,

        atrasadas=parcelas_atrasadas,

        veiculos_livres=veiculos_livres,

        ultimas_locacoes=ultimas_locacoes,

        ultimas_parcelas=ultimas_parcelas,

        negociacoes=[]

    )