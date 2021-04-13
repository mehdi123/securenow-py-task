import json
from flask import Flask, request, jsonify
from database import querier
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello'

@app.route('/api/v1/customer', methods=['PUT'])
def create_customer():
    customer = json.loads(request.data)
    if querier.create_customer(**customer):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route('/api/v1/customer', methods=['POST'])
def update_customer():
    data = json.loads(request.data)
    if querier.update_customer(**data):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route('/api/v1/customer', methods=['DELETE'])
def delete_customer():
    data = json.loads(request.data)
    if querier.delete_customer(**data):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route('/api/v1/customer', methods=['GET']):
def get_customer():
    _id = request.args.get('id')
    return jsonify(querier.get_customer(_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')