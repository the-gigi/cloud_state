import os
import json
from flask import Flask, send_from_directory, request, jsonify

app = Flask(__name__)

header = []
cloudState = {}

def csvify(rows):
    with open(os.path.join(app.static_folder, 'cloudState.csv'), 'w') as f:
        lines = [','.join((str(item) for item in row)) for row in rows]
        f.write('\n'.join(lines))

    return send_from_directory(app.static_folder, 'cloudState.csv', as_attachment=True)

@app.route('/')
def index():
    return 'Hi there!'

@app.route('/report/<ip>', methods = ['POST'])
def reportServerState(ip):
    data = json.loads(request.data)
    #assert isinstance(data, dict)
    if not header:
        header.extend(data.keys())

    cloudState[ip] = data.values()

    return "OK"

@app.route('/snapshot/<format>')
def getCloudSnapshot(format):

    if format == 'csv':
        return csvify([header] + cloudState.values())
    elif format == 'json':
        state = [dict(zip(header, row)) for row in cloudState.values()]
        return jsonify(dict(state=state))
    else:
        raise Exception('Unknown format: ' + str(format))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', -1))
    if port == -1:
        app.run(debug=True, port=8000)
    else:
        app.run(debug=True, host='0.0.0.0', port=port)

