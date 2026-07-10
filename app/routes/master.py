import secrets
import string

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user, login_user

from app import db
from app.models.conta import Conta
from app.models.usuario import Usuario


master_bp = Blueprint("master", __name__)


def master_required():
    return current_user.is_authenticated and current_user.perfil == "MASTER"


def gerar_senha(tamanho=10):
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(tamanho))


@master_bp.route("/master")
@login_required
def dashboard():
    if not master_required():
        return "Acesso negado.", 403

    total_contas = Conta.query.count()
    total_usuarios = Usuario.query.count()

    return render_template(
        "master/dashboard.html",
        total_contas=total_contas,
        total_usuarios=total_usuarios,
        total_clientes=0,
        total_veiculos=0,
        total_locacoes=0,
        total_recebimentos=0
    )


@master_bp.route("/master/contas")
@login_required
def contas():
    if not master_required():
        return "Acesso negado.", 403

    busca = request.args.get("busca", "").strip()
    status = request.args.get("status", "").strip()
    plano = request.args.get("plano", "").strip()

    query = Conta.query

    if busca:
        query = query.filter(Conta.nome.ilike(f"%{busca}%"))

    if status:
        query = query.filter_by(status=status)

    if plano:
        query = query.filter_by(plano=plano)

    contas = query.order_by(Conta.data_cadastro.desc()).all()

    return render_template(
        "master/contas.html",
        contas=contas,
        busca=busca,
        status=status,
        plano=plano,
        total_contas=Conta.query.count(),
        total_ativas=Conta.query.filter_by(status="ativo").count(),
        total_teste=Conta.query.filter_by(status="teste").count(),
        total_bloqueadas=Conta.query.filter_by(status="bloqueado").count()
    )


@master_bp.route("/master/contas/nova", methods=["POST"])
@login_required
def nova_conta():
    if not master_required():
        return "Acesso negado.", 403

    nome = request.form.get("nome", "").strip()
    cpf_cnpj = request.form.get("cpf_cnpj", "").strip()
    telefone = request.form.get("telefone", "").strip()
    email = request.form.get("email", "").strip().lower()
    plano = request.form.get("plano", "basico").strip()
    status = request.form.get("status", "ativo").strip()

    admin_nome = request.form.get("admin_nome", "").strip()
    admin_email = request.form.get("admin_email", "").strip().lower()
    admin_senha = request.form.get("admin_senha", "").strip()

    if not nome:
        flash("Informe o nome da conta.", "warning")
        return redirect(url_for("master.contas"))

    if not admin_nome or not admin_email:
        flash("Informe nome e e-mail do ADMIN.", "warning")
        return redirect(url_for("master.contas"))

    if Usuario.query.filter_by(email=admin_email).first():
        flash("Já existe um usuário com esse e-mail de ADMIN.", "danger")
        return redirect(url_for("master.contas"))

    senha_gerada = False

    if not admin_senha:
        admin_senha = gerar_senha()
        senha_gerada = True

    conta = Conta(
        nome=nome,
        cpf_cnpj=cpf_cnpj,
        telefone=telefone,
        email=email,
        plano=plano,
        status=status
    )

    db.session.add(conta)
    db.session.flush()

    admin = Usuario(
        conta_id=conta.id,
        nome=admin_nome,
        email=admin_email,
        perfil="ADMIN",
        ativo=(status != "bloqueado")
    )
    admin.set_senha(admin_senha)

    db.session.add(admin)
    db.session.commit()

    if senha_gerada:
        flash(f"Conta criada com sucesso. Senha do ADMIN: {admin_senha}", "success")
    else:
        flash("Conta criada com sucesso.", "success")

    return redirect(url_for("master.contas"))


@master_bp.route("/master/contas/<int:conta_id>/editar", methods=["POST"])
@login_required
def editar_conta(conta_id):
    if not master_required():
        return "Acesso negado.", 403

    conta = Conta.query.get_or_404(conta_id)

    conta.nome = request.form.get("nome", "").strip()
    conta.cpf_cnpj = request.form.get("cpf_cnpj", "").strip()
    conta.telefone = request.form.get("telefone", "").strip()
    conta.email = request.form.get("email", "").strip().lower()
    conta.plano = request.form.get("plano", "basico").strip()
    conta.status = request.form.get("status", "ativo").strip()

    usuarios = Usuario.query.filter_by(conta_id=conta.id).all()
    for usuario in usuarios:
        usuario.ativo = conta.status != "bloqueado"

    db.session.commit()

    flash("Conta atualizada com sucesso.", "success")
    return redirect(url_for("master.contas"))


@master_bp.route("/master/contas/<int:conta_id>/resetar-senha", methods=["POST"])
@login_required
def resetar_senha_admin(conta_id):
    if not master_required():
        return "Acesso negado.", 403

    conta = Conta.query.get_or_404(conta_id)
    admin = Usuario.query.filter_by(conta_id=conta.id, perfil="ADMIN").first()

    if not admin:
        flash("Essa conta não possui usuário ADMIN.", "danger")
        return redirect(url_for("master.contas"))

    nova_senha = gerar_senha()
    admin.set_senha(nova_senha)
    admin.ativo = True

    db.session.commit()

    flash(f"Senha resetada para {admin.email}: {nova_senha}", "success")
    return redirect(url_for("master.contas"))


@master_bp.route("/master/contas/<int:conta_id>/bloquear", methods=["POST"])
@login_required
def bloquear_conta(conta_id):
    if not master_required():
        return "Acesso negado.", 403

    conta = Conta.query.get_or_404(conta_id)
    conta.status = "bloqueado"

    for usuario in Usuario.query.filter_by(conta_id=conta.id).all():
        usuario.ativo = False

    db.session.commit()

    flash("Conta bloqueada com sucesso.", "warning")
    return redirect(url_for("master.contas"))


@master_bp.route("/master/contas/<int:conta_id>/ativar", methods=["POST"])
@login_required
def ativar_conta(conta_id):
    if not master_required():
        return "Acesso negado.", 403

    conta = Conta.query.get_or_404(conta_id)
    conta.status = "ativo"

    for usuario in Usuario.query.filter_by(conta_id=conta.id).all():
        usuario.ativo = True

    db.session.commit()

    flash("Conta ativada com sucesso.", "success")
    return redirect(url_for("master.contas"))


@master_bp.route("/master/contas/<int:conta_id>/entrar")
@login_required
def entrar_como_admin(conta_id):
    if not master_required():
        return "Acesso negado.", 403

    conta = Conta.query.get_or_404(conta_id)

    if conta.status == "bloqueado":
        flash("Não é possível acessar uma conta bloqueada.", "warning")
        return redirect(url_for("master.contas"))

    admin = Usuario.query.filter_by(conta_id=conta.id, perfil="ADMIN", ativo=True).first()

    if not admin:
        flash("Nenhum ADMIN ativo encontrado para essa conta.", "danger")
        return redirect(url_for("master.contas"))

    session["master_original_id"] = current_user.id
    login_user(admin)

    flash(f"Você entrou como ADMIN da conta {conta.nome}.", "info")
    return redirect("/dashboard")


@master_bp.route("/voltar-master")
@login_required
def voltar_master():
    master_id = session.get("master_original_id")

    if not master_id:
        return redirect("/")

    master = db.session.get(Usuario, int(master_id))

    if not master or master.perfil != "MASTER":
        session.pop("master_original_id", None)
        return redirect("/")

    login_user(master)
    session.pop("master_original_id", None)

    flash("Você voltou para o painel MASTER.", "success")
    return redirect(url_for("master.contas"))