from datetime import date, datetime

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app import db
from app.models.pagamento import Pagamento
from app.models.parcela import Parcela


recebimentos_bp = Blueprint(
    "recebimentos",
    __name__,
    url_prefix="/recebimentos"
)


@recebimentos_bp.route("/")
@login_required
def listar():

    hoje = date.today()

    forma = (
        request.args.get("forma") or ""
    ).strip().lower()

    query = Pagamento.query.filter_by(
        conta_id=current_user.conta_id
    )

    if forma:
        query = query.filter(
            db.func.lower(
                Pagamento.forma_pagamento
            ) == forma
        )

    pagamentos = query.order_by(
        Pagamento.id.desc()
    ).all()

    # Somente pagamentos confirmados entram nos totais.
    pagamentos_confirmados = [
        pagamento
        for pagamento in pagamentos
        if pagamento.webhook_recebido is True
    ]

    total_geral = sum(
        float(pagamento.valor or 0)
        for pagamento in pagamentos_confirmados
    )

    total_hoje = sum(
        float(pagamento.valor or 0)
        for pagamento in pagamentos_confirmados
        if pagamento.data_pagamento
        and pagamento.data_pagamento.date() == hoje
    )

    total_pix = sum(
        float(pagamento.valor or 0)
        for pagamento in pagamentos_confirmados
        if (
            pagamento.forma_pagamento or ""
        ).lower() in {
            "pix",
            "pix manual"
        }
    )

    total_pendentes = sum(
        1
        for pagamento in pagamentos
        if pagamento.webhook_recebido is not True
    )

    return render_template(
        "recebimentos/listar.html",
        pagamentos=pagamentos,
        total_geral=total_geral,
        total_hoje=total_hoje,
        total_pix=total_pix,
        total_pendentes=total_pendentes,
        forma=forma
    )


@recebimentos_bp.route("/<int:pagamento_id>")
@login_required
def detalhes_recebimento(pagamento_id):

    pagamento = Pagamento.query.filter_by(
        id=pagamento_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    parcela = pagamento.parcela

    return render_template(
        "recebimentos/detalhes_recebimento.html",
        pagamento=pagamento,
        parcela=parcela
    )


@recebimentos_bp.route(
    "/<int:pagamento_id>/confirmar"
)
@login_required
def confirmar_pix(pagamento_id):

    pagamento = Pagamento.query.filter_by(
        id=pagamento_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    parcela = pagamento.parcela

    if not pagamento.comprovante:

        flash(
            "Este pagamento não possui comprovante anexado.",
            "danger"
        )

        return redirect(
            url_for(
                "recebimentos.detalhes_recebimento",
                pagamento_id=pagamento.id
            )
        )

    if pagamento.webhook_recebido is True:

        flash(
            "Este recebimento já foi confirmado.",
            "warning"
        )

        return redirect(
            url_for(
                "recebimentos.detalhes_recebimento",
                pagamento_id=pagamento.id
            )
        )

    agora = datetime.utcnow()

    # Confirma o pagamento existente.
    pagamento.webhook_recebido = True
    pagamento.gateway = pagamento.gateway or "Manual"
    pagamento.forma_pagamento = "pix"
    pagamento.data_pagamento = agora

    texto = "Pagamento PIX confirmado manualmente pela locadora."

    if pagamento.observacoes:
        pagamento.observacoes += "\n\n" + texto
    else:
        pagamento.observacoes = texto

    # Baixa a parcela.
    parcela.status = "paga"
    parcela.valor_recebido = pagamento.valor
    parcela.forma_pagamento = "PIX Manual"
    parcela.data_pagamento = agora.date()

    db.session.commit()

    flash(
        "Pagamento confirmado e parcela baixada com sucesso.",
        "success"
    )

    return redirect(
        url_for(
            "recebimentos.detalhes_recebimento",
            pagamento_id=pagamento.id
        )
    )


@recebimentos_bp.route(
    "/<int:pagamento_id>/recusar"
)
@login_required
def recusar_pix(pagamento_id):

    pagamento = Pagamento.query.filter_by(
        id=pagamento_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    if pagamento.webhook_recebido is True:

        flash(
            "Um recebimento confirmado não pode ser recusado.",
            "danger"
        )

        return redirect(
            url_for(
                "recebimentos.detalhes_recebimento",
                pagamento_id=pagamento.id
            )
        )

    # Como o model ainda não possui status próprio,
    # removemos somente a informação pendente.
    # O cliente poderá enviar novamente.
    db.session.delete(pagamento)
    db.session.commit()

    flash(
        "Comprovante recusado. O cliente poderá enviar novamente.",
        "warning"
    )

    return redirect(
        url_for("recebimentos.listar")
    )