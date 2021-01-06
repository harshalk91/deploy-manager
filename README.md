# deploy-manager
pip3 install -r requirements
docker run -dit -p 6379:6379 --name some-redis redis
docker run -dit -p 27017:27017 --name some-mongo -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=secret mongo

API
python3 app.py

Worker
celery -A app.celery worker --loglevel=DEBUG
