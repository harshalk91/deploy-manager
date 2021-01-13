import logging
import os
import yaml
from flask import Flask
from werkzeug.utils import import_string

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
BLUEPRINT_CONFIG = APP_ROOT + '/blueprint_configs'

app = Flask(__name__)

for dirpath, dnames, fnames in os.walk(BLUEPRINT_CONFIG):
    for f in fnames:
        f_yml = yaml.safe_load(open(os.path.join(dirpath, f), 'r'))

        if 'blueprints' in f_yml:
            for blueprint in f_yml.get('blueprints'):
                bprint = import_string(f'blueprints.{blueprint}.bp')
                app.register_blueprint(bprint)

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.logger.setLevel(logging.DEBUG)
app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
