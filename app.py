from controllers.square2D import sq2d_bp
from controllers.triangle2D import tri2d_bp
from controllers.calculation import CalculationNamespace


from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, logger=True)

@app.route('/')
def index():
    return render_template("common2D.html", ns="square2D")

app.register_blueprint(sq2d_bp)
app.register_blueprint(tri2d_bp)
socketio.on_namespace(CalculationNamespace('/calculation'))

if __name__ == "__main__":
    socketio.run(app, debug=True)
