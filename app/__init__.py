import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from config import config, Config

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
migrate = Migrate()
jwt = JWTManager()


def error_handler(e):
    return "Something bad happened", 400


def identity(payload):
    return None


def user_loader(payload):
    return None
    # return Agent.query.filter(Agent.username == payload).first()


def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app(config_name: str = None):
    conf = config[config_name] if config_name else get_config()

    app = Flask(__name__)

    cors.init_app(app)

    app.config.from_object(conf)
    conf.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql://%s:%s@%s:%s/%s' % (app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_HOST'],
                                    app.config['MYSQL_PORT'], app.config['MYSQL_DB'])

    db.init_app(app)

    # set migration
    migrate.init_app(app, db)

    # allow following migration commands
    # $ flask db stamp head
    # $ flask db migrate
    # $ flask db upgrade
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    # with app.app_context():
    #     db.create_all()

    jwt.user_identity_loader(identity)
    jwt.user_loader_callback_loader(user_loader)

    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    jwt.init_app(app=app)

    bcrypt.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
