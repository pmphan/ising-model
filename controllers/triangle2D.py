from flask import Blueprint, render_template, request

from service.triangle2D import Triangle2D
from service.serialization import serialize_array, serialize_plot

tri2d_bp = Blueprint(
    name='triangle2D',
    import_name=__name__,
    static_folder='static',
    template_folder='templates/triangle2D',
    url_prefix='/triangle2D'
)

@tri2d_bp.route("/")
def index():
    return render_template("common2D.html", ns="triangle2D")

@tri2d_bp.route("/plot_lattice", methods=["POST"])
def plot_lattice():
    N = int(request.form.get('ndim', 2))
    kT = float(request.form.get('ktemp', 2.0))
    lattice = Triangle2D(N, kT)
    array = lattice.lattice

    title = f"2D Square Lattice {N}x{N}, kT={kT}"
    serialized_plot = Triangle2D.plot_lattice(array, title, serialize_plot)

    serialized_array = serialize_array(array)

    return {
        "plot": serialized_plot,
        "array": serialized_array,
    }
