from flask import Blueprint, render_template
from flask_login import login_required, current_user


analysis_center_bp = Blueprint(
    "analysis_center",
    __name__
)


@analysis_center_bp.route("/analysis-center")
@login_required
def index():

    if current_user.perfil != "ADMIN":
        return "Acesso não autorizado.", 403

    return render_template(
        "analysis_center/index.html"
    )