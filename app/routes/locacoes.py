from datetime import datetime, timedelta

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from app import db

from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.locacao import Locacao
from app.models.parcela import Parcela
from app.models.pagamento import Pagamento
from app.models.negociacao import Negociacao

from flask import send_file
from io import BytesIO

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


locacoes_bp = Blueprint(
    "locacoes",
    __name__
)


@locacoes_bp.route("/locacoes")
@login_required
def listar_locacoes():

    locacoes = Locacao.query.filter_by(
        conta_id=current_user.conta_id
    ).order_by(
        Locacao.id.desc()
    ).all()

    return render_template(
        "locacoes/listar.html",
        locacoes=locacoes
    )


@locacoes_bp.route("/locacoes/<int:locacao_id>")
@login_required
def detalhes_locacao(locacao_id):

    locacao = Locacao.query.filter_by(
        id=locacao_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    parcelas = Parcela.query.filter_by(
        locacao_id=locacao.id
    ).order_by(
        Parcela.numero.asc()
    ).all()

    return render_template(
        "locacoes/detalhes.html",
        locacao=locacao,
        parcelas=parcelas
    )


@locacoes_bp.route(
"/locacoes/<int:locacao_id>/contrato"
)
@login_required
def contrato_pdf(locacao_id):

    locacao = Locacao.query.filter_by(
        id=locacao_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elementos = []

    titulo = Paragraph(

        "<b><font size='18'>77 FROTAS</font></b>",

        styles["Title"]

    )

    elementos.append(titulo)

    elementos.append(Spacer(1,20))

    elementos.append(

        Paragraph(

            "<b>CONTRATO DE LOCAÇÃO</b>",

            styles["Heading2"]

        )

    )

    elementos.append(Spacer(1,20))

    elementos.append(

        Paragraph(

            f"<b>Cliente:</b> {locacao.cliente.nome}",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"<b>Veículo:</b> {locacao.veiculo.marca} {locacao.veiculo.modelo}",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"<b>Placa:</b> {locacao.veiculo.placa}",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"<b>Plano:</b> {locacao.plano}",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"<b>Valor:</b> R$ {locacao.valor_diaria:.2f}",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"<b>Data:</b> {locacao.data_inicio.strftime('%d/%m/%Y')}",

            styles["Normal"]

        )

    )

    elementos.append(Spacer(1,40))

    elementos.append(

        Paragraph(

            "________________________________________",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            "Assinatura do Cliente",

            styles["Normal"]

        )

    )

    doc.build(elementos)

    buffer.seek(0)

    return send_file(

        buffer,

        as_attachment=False,

        download_name=f"Contrato_{locacao.id}.pdf",

        mimetype="application/pdf"

    )


@locacoes_bp.route(
    "/locacoes/<int:locacao_id>/recibo"
)
@login_required
def recibo_pdf(locacao_id):

    locacao = Locacao.query.filter_by(
        id=locacao_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(

        Paragraph(

            "<b><font size='18'>77 FROTAS</font></b>",

            styles["Title"]

        )

    )

    elementos.append(Spacer(1,20))

    elementos.append(

        Paragraph(

            "<b>RECIBO DE PAGAMENTO</b>",

            styles["Heading2"]

        )

    )

    elementos.append(Spacer(1,20))

    elementos.append(

        Paragraph(

            f"Recebemos de <b>{locacao.cliente.nome}</b>",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"Referente à locação do veículo <b>{locacao.veiculo.marca.nome} {locacao.veiculo.modelo.nome}</b>",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"Placa: <b>{locacao.veiculo.placa}</b>",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"Plano: <b>{locacao.plano}</b>",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"Valor: <b>R$ {locacao.valor_diaria:.2f}</b>",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            f"Data: <b>{datetime.today().strftime('%d/%m/%Y')}</b>",

            styles["Normal"]

        )

    )

    elementos.append(Spacer(1,50))

    elementos.append(

        Paragraph(

            "________________________________________",

            styles["Normal"]

        )

    )

    elementos.append(

        Paragraph(

            "77 FROTAS",

            styles["Normal"]

        )

    )

    doc.build(elementos)

    buffer.seek(0)

    return send_file(

        buffer,

        as_attachment=False,

        download_name=f"Recibo_{locacao.id}.pdf",

        mimetype="application/pdf"

    )


@locacoes_bp.route(
"/locacoes/<int:locacao_id>/encerrar",
methods=["GET", "POST"]
)
@login_required
def encerrar_locacao(locacao_id):

    locacao = Locacao.query.filter_by(
        id=locacao_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    if request.method == "POST":

        locacao.status = "encerrada"
        locacao.data_fim = datetime.today()
        locacao.observacoes = request.form.get("observacoes")

        locacao.veiculo.status = "disponivel"
        locacao.veiculo.km_atual = int(
            request.form.get("km_devolucao") or locacao.veiculo.km_atual or 0
        )

        db.session.commit()

        flash(
            "Locação encerrada com sucesso.",
            "success"
        )

        return redirect(
            url_for(
                "locacoes.detalhes_locacao",
                locacao_id=locacao.id
            )
        )

    return render_template(
        "locacoes/encerrar.html",
        locacao=locacao
    )


@locacoes_bp.route(
    "/locacoes/nova",
    methods=["GET", "POST"]
)
@login_required
def nova_locacao():

    if request.method == "POST":

        cliente_id = request.form.get("cliente_id")
        veiculo_id = request.form.get("veiculo_id")

        plano = request.form.get("plano")

        valor_total = float(
            request.form.get("valor_locacao") or 0
        )

        quantidade = int(
            request.form.get(
                "quantidade_parcelas",
                1
            )
        )

        primeiro_vencimento = request.form.get(
            "primeiro_vencimento"
        )

        if primeiro_vencimento:

            vencimento = datetime.strptime(
                primeiro_vencimento,
                "%Y-%m-%d"
            ).date()

        else:

            vencimento = datetime.today().date()

        cliente = Cliente.query.filter_by(
            id=cliente_id,
            conta_id=current_user.conta_id
        ).first_or_404()

        veiculo = Veiculo.query.filter_by(
            id=veiculo_id,
            conta_id=current_user.conta_id
        ).first_or_404()

        # ==========================
        # Segurança
        # ==========================

        if veiculo.status != "disponivel":

            flash(
                "Este veículo não está mais disponível.",
                "warning"
            )

            return redirect(
                url_for("locacoes.nova_locacao")
            )

            locacao_ativa = Locacao.query.filter_by(
                conta_id=current_user.conta_id,
                veiculo_id=veiculo.id,
                status="ativa"
            ).first()

            if locacao_ativa:

                flash(
                    "Este veículo já possui uma locação ativa.",
                    "warning"
                )

                return redirect(
                    url_for("locacoes.nova_locacao")
                )

        # ==========================
        # Cria Locação
        # ==========================

        locacao = Locacao(

            conta_id=current_user.conta_id,

            cliente_id=cliente.id,

            veiculo_id=veiculo.id,

            data_inicio=datetime.today().date(),

            plano=plano,

            valor_diaria=valor_total,

            status="ativa"

        )

        db.session.add(locacao)

        # ==========================
        # Intervalo das cobranças
        # ==========================

        if plano == "Diária":

            intervalo = 1

        elif plano == "Semanal":

            intervalo = 7

        elif plano == "Quinzenal":

            intervalo = 15

        else:

            # Mensal
            intervalo = 30

        # ==========================
        # Geração das parcelas
        # ==========================

        for numero in range(1, quantidade + 1):

            venc = vencimento + timedelta(
                days=(numero - 1) * intervalo
            )

            parcela = Parcela(
                conta_id=current_user.conta_id,
                locacao=locacao,
                numero=numero,
                vencimento=venc,
                valor=valor_total,
                status="aberta"
            )

            db.session.add(parcela)

        # ==========================
        # Atualiza veículo
        # ==========================

        veiculo.status = "locado"

        db.session.commit()

        flash(
            "Locação criada com sucesso.",
            "success"
        )

        return redirect(
            url_for(
                "locacoes.listar_locacoes"
            )
        )

    clientes = Cliente.query.filter_by(
        conta_id=current_user.conta_id
    ).all()

    veiculos = Veiculo.query.filter_by(
        conta_id=current_user.conta_id,
        status="disponivel"
    ).all()

    return render_template(
        "locacoes/wizard.html",
        clientes=clientes,
        veiculos=veiculos
    )


@locacoes_bp.route(
    "/parcelas/<int:parcela_id>/receber",
    methods=["GET", "POST"]
)
@login_required
def receber_parcela(parcela_id):

    parcela = Parcela.query.filter_by(
        id=parcela_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    if request.method == "POST":

        valor_recebido = float(
            request.form.get("valor_recebido") or parcela.valor
        )

        parcela.status = "paga"

        parcela.data_pagamento = datetime.today().date()

        parcela.forma_pagamento = request.form.get(
            "forma_pagamento"
        )

        parcela.valor_recebido = valor_recebido

        parcela.juros = float(
            request.form.get("juros") or 0
        )

        parcela.multa = float(
            request.form.get("multa") or 0
        )

        parcela.desconto = float(
            request.form.get("desconto") or 0
        )

        parcela.observacoes = request.form.get(
            "observacoes"
        )

        pagamento = Pagamento(
            conta_id=current_user.conta_id,
            parcela_id=parcela.id,
            valor=valor_recebido,
            forma_pagamento=parcela.forma_pagamento
        )

        db.session.add(pagamento)

        db.session.commit()

        flash(
            "Pagamento registrado com sucesso.",
            "success"
        )

        return redirect(
            url_for(
                "locacoes.detalhes_locacao",
                locacao_id=parcela.locacao_id
            )
        )

    return render_template(
        "parcelas/receber.html",
        parcela=parcela
    )


@locacoes_bp.route(
    "/parcelas/<int:parcela_id>/negociar",
    methods=["GET", "POST"]
)
@login_required
def negociar_parcela(parcela_id):

    parcela = Parcela.query.filter_by(
        id=parcela_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    if request.method == "POST":

        novo_valor = float(
            request.form.get("novo_valor") or parcela.valor
        )

        novo_vencimento = datetime.strptime(
            request.form.get("novo_vencimento"),
            "%Y-%m-%d"
        ).date()

        juros = float(
            request.form.get("juros") or 0
        )

        multa = float(
            request.form.get("multa") or 0
        )

        desconto = float(
            request.form.get("desconto") or 0
        )

        observacoes = request.form.get(
            "observacoes"
        )

        negociacao = Negociacao(

            conta_id=current_user.conta_id,

            parcela_id=parcela.id,

            valor_original=parcela.valor,

            novo_valor=novo_valor,

            vencimento_original=parcela.vencimento,

            novo_vencimento=novo_vencimento,

            juros=juros,

            multa=multa,

            desconto=desconto,

            observacoes=observacoes,

            status="ativa"

        )

        db.session.add(negociacao)

        parcela.valor = novo_valor

        parcela.vencimento = novo_vencimento

        parcela.juros = juros

        parcela.multa = multa

        parcela.desconto = desconto

        parcela.observacoes = observacoes

        parcela.status = "aberta"

        db.session.commit()

        flash(
            "Negociação realizada com sucesso.",
            "success"
        )

        return redirect(
            url_for(
                "locacoes.detalhes_locacao",
                locacao_id=parcela.locacao_id
            )
        )

    return render_template(
        "parcelas/negociar.html",
        parcela=parcela
    )
    

@locacoes_bp.route(
    "/parcelas/<int:parcela_id>/historico"
)
@login_required
def historico_negociacao(parcela_id):

    parcela = Parcela.query.filter_by(
        id=parcela_id,
        conta_id=current_user.conta_id
    ).first_or_404()

    negociacoes = Negociacao.query.filter_by(
        parcela_id=parcela.id
    ).order_by(
        Negociacao.data_negociacao.desc()
    ).all()

    return render_template(
        "parcelas/historico_negociacao.html",
        parcela=parcela,
        negociacoes=negociacoes
    )