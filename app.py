from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    beam_length = data['beam_length']
    point_loads = data['point_loads']
    udls = data['udls']

    # Calculate support reactions (simply supported beam)
    moment_sum = 0.0
    vertical_load_sum = 0.0
    for load in point_loads:
        vertical_load_sum += load['magnitude']
        moment_sum += load['magnitude'] * load['position']
    for udl in udls:
        length_udl = udl['end'] - udl['start']
        load_total = udl['magnitude'] * length_udl
        vertical_load_sum += load_total
        moment_sum += load_total * (udl['start'] + length_udl / 2)
    Rb = moment_sum / beam_length
    Ra = vertical_load_sum - Rb

    x = np.linspace(0, beam_length, 500)
    shear = np.zeros_like(x)
    moment = np.zeros_like(x)

    for i, xi in enumerate(x):
        V = Ra
        M = Ra * xi
        for load in point_loads:
            if xi >= load['position']:
                V -= load['magnitude']
                M -= load['magnitude'] * (xi - load['position'])
        for udl in udls:
            if xi >= udl['start']:
                length_seg = min(xi, udl['end']) - udl['start']
                if length_seg > 0:
                    load_seg = udl['magnitude'] * length_seg
                    V -= load_seg
                    M -= load_seg * (xi - (udl['start'] + length_seg / 2))
        shear[i] = V
        moment[i] = M

    result = {
        'Ra': Ra,
        'Rb': Rb,
        'x': x.tolist(),
        'shear': shear.tolist(),
        'moment': moment.tolist()
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
