from flask import request
from flask_socketio import Namespace, emit, disconnect

from service.serialization import deserialize_array, serialize_plot
from service.square2D import Square2D
from service.triangle2D import Triangle2D

class CalculationNamespace(Namespace):
    disconnected_clients = set()

    class_mapping = {
        "square2D": Square2D,
        "triangle2D": Triangle2D
    }

    def on_calculate(self, data):
        params : dict[str, str] = {}
        for kv in data:
            params[kv['name']] = kv['value']
        N = int(params['ndim'])
        kT = float(params['ktemp'])
        nstep = int(params['nstep'])
        nyield = int(params['nimg'])
        array = deserialize_array(params['array'])
        Class2D = self.class_mapping[params['ns']]
        for result, i in Class2D.metropolis(array, kT, nstep, nyield):
            # Early termination
            if request.sid in self.disconnected_clients:
                self.disconnected_clients.remove(request.sid)
                break
            title = f"{N}x{N} result at step {i} with kT={kT}"
            splot = Class2D.plot_lattice(result, title, serialize_plot)
            emit("calculating", {'i': i, 'plot': splot})

        emit("calculated")

    def on_stop(self):
        self.disconnected_clients.add(request.sid)

    def on_disconnect(self):
        disconnect()
        self.disconnected_clients.add(request.sid)
