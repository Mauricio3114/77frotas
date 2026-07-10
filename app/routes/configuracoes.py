from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db

configuracoes_bp = Blueprint(
    "configuracoes",
    __name__,
    url_prefix="/configuracoes"
)


@configuracoes_bp.route("/pix", methods=["GET", "POST"])
@login_required
def pix():

    conta = current_user.conta

    if request.method == "POST":

        conta.tipo_chave_pix = request.form.get(
            "tipo_chave_pix"
        )

        conta.chave_pix = request.form.get(
            "chave_pix"
        )

        conta.favorecido_pix = request.form.get(
            "favorecido_pix"
        )

        conta.banco_pix = request.form.get(
            "banco_pix"
        )

        db.session.commit()

        flash(
            "Configuração PIX salva com sucesso.",
            "success"
        )

        return redirect(
            url_for("configuracoes.pix")
        )

    return render_template(
        "configuracoes/pix.html",
        conta=conta
    )