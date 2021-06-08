from flask import Flask, json, request, jsonify, render_template
import flask
from bson import json_util
from app import app
from app import db
from flask_httpauth import HTTPTokenAuth
from .function import functions
from .usuarios import user_functions
from bson.objectid import ObjectId
import base64
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "qalqwe": "sadfsadfjoi",
}


@auth.verify_token
def verify_token(token):
    print(token)
    print(tokens)
    if token in tokens:
        return tokens[token]

@auth.error_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401


@app.route('/index', methods=['POST'])
@auth.login_required
def index():
    json_data = request.json
    if json_data is not None:
        userId = json_data["id"]
        return flask.jsonify(json.loads(json_util.dumps(db.agenda.find({"userId": userId}).sort("_id", 1))))
    else:
        return jsonify(mensagem='Erro'), 404
    



@app.route('/event', methods=['POST'])
@auth.login_required
def create():
    json_data = request.json
    if json_data is not None:
        name = json_data["name"]
        details = json_data["details"]
        start = json_data["start"]
        end = json_data["end"]
        color = json_data["color"]
        userId = json_data["userId"]
        result = functions.salvarNovo(name, details, start, end, color, userId)
        if result != False:
            return jsonify(mensagem='Evento criado')
        else:
            return jsonify(mensagem='Evento não criado'), 404
    else:
        return jsonify(mensagem='Evento não criado'), 404




@app.route('/event', methods=['DELETE'])
@auth.login_required
def delete():
    json_data = request.json
    if json_data is not None:
        id = json_data["id"]
        result = functions.salvarDelecao(id)
        if result == True:
            return flask.jsonify(json.loads(json_util.dumps({"result": result})))
        else:
            return jsonify(mensagem='Evento não deletado')
    else:
        return flask.jsonify(json.loads(json_util.dumps({"result": False}))), 404



@app.route('/event', methods=['PUT'])
@auth.login_required
def update():
    json_data = request.json
    if json_data is not None:
        print(json_data)
        id = json_data["id"]
        name = json_data["name"]
        details = json_data["details"]
        start = json_data["start"]
        end = json_data["end"]
        color = json_data["color"]
        result = functions.salvarEdicao(id, name, details, start, end, color)
        if result != False:
            return flask.jsonify(json.loads(json_util.dumps({"result": result})))
        else:
            return flask.jsonify(json.loads(json_util.dumps({"result": False}))), 404
    else:
        return flask.jsonify(json.loads(json_util.dumps({"result": False}))), 404


@app.route('/registro', methods=['POST'])
def create_user():
    json_data = request.json
    if json_data is not None:
        email = str(json_data["email"])
        senha = json_data["senha"]
        if email.count('@') == 1 and email.count('.') >= 1:
            email = email.strip()
            if email[-1] == '.':
                email = email[0:-1]
            email = str(email.replace(',', '').replace(
                ';', '').replace('!', '').replace('"', '').replace("'", ''))
            result = user_functions.salvarNovo(
                email, senha)
            if result != False:
                return jsonify(mensagem='Usuario criado')
            else:
                return jsonify(mensagem='Usuario não criado'), 404
        else:
            return jsonify(mensagem='Usuario não criado'), 404
    else:
        return jsonify(mensagem='Usuario não criado'), 404


def getCODE():
    from datetime import datetime
    dataHora = datetime.now()
    code = str(dataHora.year)
    code += str(dataHora.month)
    code += str(dataHora.day)
    code += str(dataHora.hour)
    code += str(dataHora.minute)
    code += str(dataHora.second)
    code = str(int(round(int(code)/2, 0)))
    return code


@app.route('/login', methods=['POST'])
def login():
    json_data = request.json
    if json_data is not None:
        email = str(json_data["email"])
        senha = json_data["senha"]
        if email.count('@') == 1 and email.count('.') >= 1:
            email = email.strip()
            if email[-1] == '.':
                email = email[0:-1]
            email = str(email.replace(',', '').replace(
                ';', '').replace('!', '').replace('"', '').replace("'", ''))
            result = user_functions.entrar(
                email, senha)
            if result != False:
                code = result[0].get('code')
                email = result[0].get('email')
                token = code+getCODE()+email
                token_bytes = token.encode('ascii')
                base64_bytes = base64.b64encode(token_bytes)
                base64_message = base64_bytes.decode('ascii')
                print(base64_message)
                tokens[token] = email
                print(tokens)
                return flask.jsonify(json.loads(json_util.dumps({"result": result, "token": token})))
            else:
                return jsonify(mensagem='Dados errados'), 404
        else:
            return jsonify(mensagem='Dados errados'), 404
    else:
        return jsonify(mensagem='Dados errados'), 404


@app.route('/validate', methods=['POST'])
@auth.login_required
def validate():
    json_data = request.json
    if json_data is not None:
        email = str(json_data["email"])
        id = json_data["id"]
        if email.count('@') == 1 and email.count('.') >= 1:
            email = email.strip()
            if email[-1] == '.':
                email = email[0:-1]
            email = str(email.replace(',', '').replace(
                ';', '').replace('!', '').replace('"', '').replace("'", ''))
            result = user_functions.validate(
                email, id)
            if result != False:
                return flask.jsonify(json.loads(json_util.dumps({"result": result})))
            else:
                return jsonify(mensagem='Dados errados'), 404
        else:
            return jsonify(mensagem='Dados errados'), 404
    else:
        return jsonify(mensagem='Dados errados'), 404