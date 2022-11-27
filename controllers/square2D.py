from flask import Blueprint, render_template, request
from flask_socketio import Namespace, emit, disconnect

from service.ising import Ising2D
from service.serialization import deserialize_array, serialize_array, serialize_plot

sq2d_bp = Blueprint(
    name='square2D',
    import_name=__name__,
    static_folder='static',
    template_folder='templates/square2D',
    url_prefix='/square2D'
)

@sq2d_bp.route("/")
def index():
    return render_template("square2D.html")


class CalculationNamespace(Namespace):
    disconnected_clients = set()

    def on_calculate(self, data):
        params : dict[str, str] = {}
        for kv in data:
            params[kv['name']] = kv['value']
        N = int(params['ndim'])
        kT = float(params['ktemp'])
        nstep = int(params['nstep'])
        nyield = int(params['nimg'])
        array = deserialize_array(params['array'])
        for result, i in Ising2D.metropolis(array, kT, nstep, nyield):
            # Early termination
            if request.sid in self.disconnected_clients:
                self.disconnected_clients.remove(request.sid)
                return
            title = f"{N}x{N} result at step {i} with kT={kT}"
            splot = Ising2D.plot_lattice(result, title, serialize_plot)
            emit("calculating", {'i': i, 'plot': splot})
        emit("calculated")

    def on_disconnect(self):
        disconnect()
        self.disconnected_clients.add(request.sid)

@sq2d_bp.route("/plot_lattice", methods=["POST"])
def plot_lattice():
    N = int(request.form.get('ndim', 2))
    kT = float(request.form.get('ktemp', 2.0))
    lattice = Ising2D(N, N, kT)
    array = lattice.lattice

    title = f"2D Square Lattice {N}x{N}, kT={kT}"
    serialized_plot = Ising2D.plot_lattice(array, title, serialize_plot)

    serialized_array = serialize_array(array)

    return {
        "plot": serialized_plot,
        "array": serialized_array,
    }
