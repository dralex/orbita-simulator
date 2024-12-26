# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator RESTful API
#
# The web server application
#
# Copyright (C) 2024 Alexey Fedoseev <aleksey@fedoseev.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/
# -----------------------------------------------------------------------------

from flask import Flask, request, abort, jsonify
import configparser
import orbita

SERVER_CONFIG = '/etc/orbita/rest.cfg'

cfg = configparser.ConfigParser()
cfg.read(SERVER_CONFIG)

config = cfg.get('server', 'configuration')
tempdir = cfg.get('storage', 'tempdir')
resurl = cfg.get('web', 'results')
imgurl = cfg.get('web', 'images')

app = Flask(__name__)
orbita_api = orbita.OrbitaServerAPI(config, tempdir, resurl, imgurl)

@app.route('/server', methods=['GET'])
def get_server():
    try:    
        return jsonify(orbita_api.server())
    except orbita.OrbitaNotFoundException:
        abort(404)
    except orbita.OrbitaBadRequestException:
        abort(400)

@app.route('/parameters', methods=['GET'])
def get_parameters():
    if not request.json or 'model' not in request.json or 'mission' not in request.json:
        abort(400)
    try:
        model = request.json['model']
        mission = request.json['mission']
        res = orbita_api.parameters(model, mission)
    except orbita.OrbitaNotFoundException:
        abort(404)
    except orbita.OrbitaBadRequestException:
        abort(400)
    return jsonify(res)

@app.route('/devices', methods=['GET'])
def get_devices():
    if not request.json or 'model' not in request.json:
        abort(400)
    try:
        model = request.json['model']
        res = orbita_api.devices(model)
    except orbita.OrbitaNotFoundException:
        abort(404)
    except orbita.OrbitaBadRequestException:
        abort(400)
    return jsonify(res)

@app.route('/sample', methods=['GET'])
def get_sample():
    if not request.json or 'model' not in request.json or 'mission' not in request.json:
        abort(400)
    try:
        model = request.json['model']
        mission = request.json['mission']
        res = orbita_api.sample(model, mission)
    except orbita.OrbitaNotFoundException:
        abort(404)
    except orbita.OrbitaBadRequestException:
        abort(400)
    return jsonify(res)

@app.route('/calculation', methods=['POST'])
def post_calculation():
    if not request.json or 'model' not in request.json or 'xml' not in request.json:
        abort(400)
    try:
        model = request.json['model']
        xml = request.json['xml']
        res = orbita_api.calculation(model, xml)
    except orbita.OrbitaNotFoundException:
        abort(404)
    except orbita.OrbitaBadRequestException:
        abort(400)
    return jsonify(res)

@app.route('/status', methods=['GET'])
def get_status():
    if not request.json or 'model' not in request.json or 'id' not in request.json:
        abort(400)
    try:
        model = request.json['model']
        task_id = request.json['id']
        res = orbita_api.status(model, task_id)
    except orbita.OrbitaNotFoundException:
        abort(404)
    except orbita.OrbitaBadRequestException:
        abort(400)
    return jsonify(res)

@app.route('/result', methods=['GET'])
def get_result():
    if not request.json or 'model' not in request.json or 'id' not in request.json:
        abort(400)
    try:
        model = request.json['model']
        task_id = request.json['id']
        res = orbita_api.result(model, task_id)
    except orbita.OrbitaNotFoundException:
        abort(404)
    except orbita.OrbitaBadRequestException:
        abort(400)
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
