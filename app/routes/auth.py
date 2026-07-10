from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.perfil == "MASTER":
            return redirect("/master")
        if current_user.perfil == "ADMIN":
            return redirect("/dashboard")
        if current_user.perfil == "CLIENTE":
            return redirect("/portal")

    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario or not usuario.check_senha(senha):
            flash("E-mail ou senha inválidos.", "danger")
            return redirect(url_for("auth.login"))

        if not usuario.ativo:
            flash("Usuário bloqueado.", "warning")
            return redirect(url_for("auth.login"))

        login_user(usuario)

        if usuario.perfil == "MASTER":
            return redirect("/master")
        if usuario.perfil == "ADMIN":
            return redirect("/dashboard")
        if usuario.perfil == "CLIENTE":
            return redirect("/portal")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))