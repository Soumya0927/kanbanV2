from flask import Flask
from models import db, User, List, Card
from api.api import user, list, card, user_datastore, downloadTask, summary
from flask_restful import Api
from flask_security import Security
from models import db, User, Role
from flask_cors import CORS
from flask_cache import cache
import redis
# from flask_celery import make_celery
import flask_celery1

sec = Security()

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/1',
    CELERY_RESULT_BACKEND='redis://localhost:6379/2'
)
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = '6379'
# celery = make_celery(app)
# @app.route('displayname')
# def displayname():
#    display.delay()
#    return 'async'
# @celery.task(name = 'app.display')
# def display():
#    return "mad2"
# app.config.update(result_expires=3600,     enable_utc=True,     timezone='UTC')

celery = flask_celery1.celery

celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    enable_utc=False
)

celery.Task = flask_celery1.ContextTask
cache.init_app(app)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = "thisissecret"
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'


api = Api(app)
CORS(app)
db.init_app(app)
sec.init_app(app, user_datastore)

api.add_resource(user, '/api/users')
api.add_resource(list, '/api/createlist', '/api/tasks/<string:lname>',
                 '/api/allList', '/api/editlist/<string:lname>')
api.add_resource(card, '/api/card/<int:id>',
                 '/api/<string:lname>/createcard', '/api/editcard/<int:id>')
api.add_resource(downloadTask, "/api/downloadlist/<string:lname>",
                 "/api/downloadcard/<int:id>")
api.add_resource(summary, "/api/summary")


@app.before_first_request
def create_db():
    db.create_all(app=app)


@app.route("/")
def home():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)
