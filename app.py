from flask import Flask, render_template
from services.ProviderService import ProviderService

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    provider_service_obj = ProviderService()
    providers = provider_service_obj.get_all_providers()
    return render_template('index.html', providers=providers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)