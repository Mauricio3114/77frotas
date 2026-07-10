from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models.solicitacao_negociacao import SolicitacaoNegociacao

from flask import redirect, url_for, flash
from datetime import datetime

from app import db
from app.models.negociacao import Negociacao


negociacoes_bp = Blueprint(
    "negociacoes",
    __name__,
    url_prefix="/negociacoes"
)


@negociacoes_bp.route("/solicitacoes")
@login_required
def solicitacoes():

    solicitacoes = SolicitacaoNegociacao.query.filter_by(
        conta_id=current_user.conta_id
    ).order_by(
        SolicitacaoNegociacao.id.desc()
    ).all()

    return render_template(
        "negociacoes/solicitacoes.html",
        solicitacoes=solicitacoes
    )


@negociacoes_bp.route("/solicitacoes/<int:id>")
@login_required
def detalhes_solicitacao(id):

    solicitacao = SolicitacaoNegociacao.query.get_or_404(id)

    return render_template(
        "negociacoes/detalhes_solicitacao.html",
        solicitacao=solicitacao
    )

print("ROTAS NEGOCIACOES CARREGADAS")

@negociacoes_bp.route("/solicitacoes/<int:id>/aprovar")
@login_required
def aprovar_solicitacao(id):

    solicitacao = SolicitacaoNegociacao.query.get_or_404(id)

    if solicitacao.status != "pendente":

        flash("Esta solicitação já foi analisada.", "warning")

        return redirect(
            url_for(
                "negociacoes.detalhes_solicitacao",
                id=id
            )
        )

    negociacao = Negociacao(

        conta_id=solicitacao.conta_id,

        parcela_id=solicitacao.parcela_id,

        valor_original=solicitacao.parcela.valor,

        novo_valor=solicitacao.valor_proposto,

        vencimento_original=solicitacao.parcela.vencimento,

        novo_vencimento=solicitacao.nova_data,

        observacoes=solicitacao.motivo

    )

    db.session.add(negociacao)

    solicitacao.status = "aprovada"

    solicitacao.data_resposta = datetime.utcnow()

    db.session.commit()

    flash(
        "Solicitação aprovada com sucesso.",
        "success"
    )

    return redirect(
        url_for(
            "negociacoes.detalhes_solicitacao",
            id=id
        )
    )


@negociacoes_bp.route("/solicitacoes/<int:id>/recusar")
@login_required
def recusar_solicitacao(id):

    solicitacao = SolicitacaoNegociacao.query.get_or_404(id)

    solicitacao.status = "recusada"

    solicitacao.data_resposta = datetime.utcnow()

    db.session.commit()

    flash(
        "Solicitação recusada.",
        "warning"
    )

    return redirect(
        url_for(
            "negociacoes.detalhes_solicitacao",
            id=id
        )
    )