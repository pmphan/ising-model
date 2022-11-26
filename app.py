from controllers.square2D import CalculationNamespace, sq2d_bp
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, logger=True)

@app.route('/')
def index():
    return render_template("square2D.html")

app.register_blueprint(sq2d_bp)
socketio.on_namespace(CalculationNamespace('/calculation'))

if __name__ == "__main__":
    socketio.run(app, debug=True)
