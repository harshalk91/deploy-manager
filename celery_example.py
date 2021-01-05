from flask import Flask
from flask_celery import make_celery
import logging

logging.basicConfig(
    filename="deploymanager-workflow",
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.info("Started...")
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@app.route("/process/<name>")
def process(name):
    reverse.delay(name)
    return "I set an async request"


@celery.task(name='celery_example.celery')
def reverse(string):
    return string[::-1]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
