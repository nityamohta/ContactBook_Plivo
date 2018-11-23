from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from collections import OrderedDict
import sys
app = Flask(__name__)


auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'nitya':
        return 'plivo'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

contacts =[
    {
        'name': 'nitya',
        'email': 'nityamohta@gmail.com',
        'number':8123003327,
    },
    {
        'name': 'nikita',
        'email': 'nikimohta@gmail.com',
        'number':9830085759,
    }
]


@app.route('/showall', methods=['GET'])
@auth.login_required
def get_contacts():
    return jsonify({'contacts': contacts})


@app.route('/showall/<string:name>', methods=['GET'])
@auth.login_required
def get_details(name):
    contact = [contact for contact in contacts if contact['name'] == name]
    if len(contact) == 0:
        abort(404)
    return jsonify({'contact': contact[0]})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'email already exists'}), 405)


@app.route('/insert', methods=['POST'])
@auth.login_required
def create_contact():

    contact = {
        'name': request.json['name'],
        'email': request.json['email'],
        'number': request.json['number'],
    }
    if (contact for contact in contacts if contact['email'] == contacts['email']):
        abort(405)
    else:
        contacts.append(contact)
        return jsonify({'contact': contact}), 201






@app.route('/delete/<string:name>', methods=['GET', 'POST', 'DELETE'])
@auth.login_required
def delete_contact(name):
    print('Hello world!', file=sys.stderr)
    contact = [contact for contact in contacts if contact['name'] == name]
    if len(contact) == 0:
        abort(404)
    contacts.remove(contact[0])
    return jsonify({'result': True})


@app.route('/update/<string:name>', methods=['PUT'])
@auth.login_required
def update_contact(name):
    contact = [contact for contact in contacts if contact['name'] == name]
    if len(contact) == 0:
        abort(404)
    if not request.json:
        abort(400)
    contact[0]['email'] = request.json.get('email', contact[0]['email'])
    contact[0]['number'] = request.json.get('number', contact[0]['number'])
    return jsonify({'contact': contact[0]}),201




@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

