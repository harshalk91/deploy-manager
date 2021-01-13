from flask import Flask, render_template, Blueprint, Response
from services.ProviderService import ProviderService
import os
import json

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    controller_files = []
    factories_files = []
    route_files = []

    for dirpath, dnames, fnames in os.walk("./static/js/controllers"):
        for f in fnames:
            controller_files.append(f)

    for dirpath, dnames, fnames in os.walk("./static/js/factories"):
        for f in fnames:
            factories_files.append(f)

    for dirpath, dnames, fnames in os.walk("./static/js/routes"):
        for r in fnames:
            route_files.append(r)


    return render_template('index.html',
                           controller_files=controller_files,
                           factories_files=factories_files,
                           route_files=route_files)

@bp.route('/api/config', methods=['GET'])
def get():
    try:
        provider_service_obj = ProviderService()
        providers = {'providers': provider_service_obj.get_all_providers()}
        response = json.dumps(providers)
    except Exception as e:
        response = Response(status=500, mimetype='application/json')

    return response

@bp.route('/api/config/home', methods=['GET'])
def get_home_config():
    try:
        provider_service_obj = ProviderService()
        providers = {'providers': provider_service_obj.get_all_providers()}
        response = json.dumps(providers)
    except Exception as e:
        response = Response(status=500, mimetype='application/json')

    return response