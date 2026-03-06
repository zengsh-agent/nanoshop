from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder='templates', static_folder='static')

BACKEND_URL = "http://127.0.0.1:8000"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})

    file = request.files['file']
    files = {'file': (file.filename, file.read(), file.content_type)}

    try:
        response = requests.post(f"{BACKEND_URL}/api/upload", files=files)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            data={'session_id': data['session_id'], 'message': data['message']}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/apply', methods=['POST'])
def apply():
    data = request.json
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/apply",
            data={'session_id': data['session_id'], 'operation': data['operation'], 'value': data.get('value', 1.0)}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/preview', methods=['POST'])
def preview():
    data = request.json
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/preview",
            data={'session_id': data['session_id'], 'operation': data['operation'], 'value': data.get('value', 1.0)}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/undo', methods=['POST'])
def undo():
    data = request.json
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/undo",
            data={'session_id': data['session_id']}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/reset', methods=['POST'])
def reset():
    data = request.json
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/reset",
            data={'session_id': data['session_id']}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/export', methods=['POST'])
def export():
    data = request.json
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/export",
            data={'session_id': data['session_id'], 'format': data.get('format', 'png')}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
