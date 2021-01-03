from app import app
import logging

logging.basicConfig(
    filename="deploymanager",
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.info("Started...")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.debug("wsgi")
    app.run()

