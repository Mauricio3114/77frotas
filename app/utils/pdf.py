from io import BytesIO

from flask import send_file

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)


def gerar_pdf(
    titulo,
    cabecalho,
    linhas,
    nome_arquivo
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elementos = []

    elementos.append(

        Paragraph(
            "<b>77 Frotas</b>",
            styles["Title"]
        )

    )

    elementos.append(

        Paragraph(
            titulo,
            styles["Heading2"]
        )

    )

    elementos.append(
        Spacer(1, 15)
    )

    dados = [cabecalho]

    for linha in linhas:

        dados.append(linha)

    tabela = Table(dados)

    tabela.setStyle(

        TableStyle([

            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.HexColor("#0f172a")
            ),

            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),

            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0,1),
                (-1,-1),
                colors.whitesmoke
            ),

            (
                "FONTNAME",
                (0,0),
                (-1,0),
                "Helvetica-Bold"
            ),

            (
                "BOTTOMPADDING",
                (0,0),
                (-1,0),
                10
            )

        ])

    )

    elementos.append(tabela)

    doc.build(elementos)

    buffer.seek(0)

    return send_file(

        buffer,

        as_attachment=True,

        download_name=nome_arquivo,

        mimetype="application/pdf"

    )