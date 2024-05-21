from flask import Flask, request, jsonify, g, make_response
import jwt
import requests

app = Flask(__name__)
config_file = open("./.config", "r").read().split('\n')

SECRET_KEY = config_file[0].split(' ')[1]

def verify_jwt():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized - JWT token missing"}), 401

    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        g.user = decoded
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Unauthorized - Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Unauthorized - Invalid token"}), 401
        

@app.route('/api/v1/movie/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/v1/play/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/v1/movie', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/v1/play', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/v1/movie/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/api/v1/play/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_verified(path):
    result = verify_jwt()
    if result:
        return result
    backend_response = requests.request(
        method=request.method,
        url=request.path,
        headers={key: value for key, value in request.headers if key != 'Host'},
        params=request.args,
        data=request.data
    )
    return make_response(backend_response.content, backend_response.status_code, backend_response.headers.items())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)