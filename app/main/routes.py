from flask import Blueprint, render_template
from ..models import Anuncio

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    anuncios = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc()).all()
    return render_template("main/index.html", anuncios=anuncios)