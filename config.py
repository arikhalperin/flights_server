import os


class Config:
    ENV = 'development'
    DEBUG = True
    TESTING = True
    MYSQL_HOST = '0.0.0.0'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'flights'

    @staticmethod
    def init_app(app):
        Config.the_app = app

class LocalConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    MYSQL_HOST = '0.0.0.0'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'flights'



config = {
    'local': LocalConfig,  # Localhost development environment
    'default': LocalConfig
}
