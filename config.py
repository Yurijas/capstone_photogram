import os

# define the root/base of this project folder
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # set secret key for security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    # 'postgresql://postgres:venezuel@localhost:5432/capstone'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')

    # Email
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
