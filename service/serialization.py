import numpy as np

from io import BytesIO
from base64 import b64encode, b64decode

def serialize_plot(fig):
    stream = BytesIO()
    fig.savefig(stream, transparent=True, format='png')
    serialized = b64encode(stream.getvalue()).decode('utf8')
    stream.close()
    return serialized

def serialize_array(raw: np.ndarray):
    stream = BytesIO()
    np.save(stream, raw)
    serialized = b64encode(stream.getvalue()).decode('utf8')
    stream.close()
    return serialized

def deserialize_array(serialized: str):
    stream = BytesIO()
    deserialized = b64decode(serialized.encode())
    stream.write(deserialized)
    stream.seek(0)
    raw = np.load(stream)
    stream.close()
    return raw

