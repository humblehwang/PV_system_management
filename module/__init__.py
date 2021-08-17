from flask import Flask, render_template, Blueprint
from flask_bootstrap import Bootstrap
from config import DevConfig
from module.edit import edit_api
from module.edit_non import edit_non_api
from module.search import search_api
from module.search_non import search_non_api
from module.upload import upload_api
from module.upload_non import upload_non_api
from module.control import control_api
from module.other import other_api
from module.other_non import other_non_api
from module.user import user_api
from module.search_tel import search_tel_api
from util.sql.db_init import db
import logging

app = Flask(__name__)
app.config.from_object(DevConfig)
#session key
app.secret_key = 'o\x97Ji\xa8\xd7\xfe\x9c\xb5S\xbb\xf6Bj\xad\xc2ma\xeeQ\xd7\xc4;\xb3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db config mysql://username:password@serverip/db name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://test:1234@localhost/itri?charset=utf8mb4'
app.register_blueprint(user_api, url_prefix='/')
app.register_blueprint(edit_api, url_prefix='/edit')
app.register_blueprint(edit_non_api, url_prefix='/editNon')
app.register_blueprint(search_non_api, url_prefix='/searchNon')
app.register_blueprint(search_api, url_prefix='/search')
app.register_blueprint(search_tel_api, url_prefix='/search_tel')
app.register_blueprint(upload_api, url_prefix='/upload')
app.register_blueprint(upload_non_api, url_prefix='/uploadNon')
app.register_blueprint(other_api, url_prefix='/other')
app.register_blueprint(other_non_api, url_prefix='/otherNon')
app.register_blueprint(control_api, url_prefix='/control')
Bootstrap(app)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
db.app = app
db.init_app(app)
db.create_all()

