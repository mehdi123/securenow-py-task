import json
from flask import Flask, request, jsonify
from database import querier
app = Flask(__name__)


@app.route('/api/v1/customer', methods=['PUT'])
def create_customer():
    """
    Create a new customer
    """

    customer = json.loads(request.data)
    result = querier.create_customer(**customer)
    if result:
        data_dict = {key: value for key, value in zip(("id", "name", "email", "phone", "address"), result)}
        return jsonify({"success": True, "data": data_dict})
    else:
        return jsonify({"success": False})

@app.route('/api/v1/customer', methods=['POST'])
def update_customer():
    """
        Update customer information
    """

    data = json.loads(request.data)
    if querier.update_customer(**data):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route('/api/v1/customer', methods=['DELETE'])
def delete_customer():
    """
        Delete a customer
    """

    data = json.loads(request.data)
    if querier.delete_customer(**data):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route('/api/v1/customer/<int:_id>', methods=['GET'])
def get_customer(_id):
    """
        Get customer information by id
    """

    return jsonify(querier.get_customer(_id))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')