import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    INSTANCE_NAME = 'URL Shortener'
    SECRET_KEY = 'this-is-example-secret-key-please-change-it'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SHORT_LINK_LENGTH = 7