import os

# define the root/base of this project folder
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # set secret key for security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # STRIPE_SECRET_KEY = ''

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    # 'postgresql://postgres:venezuel@localhost:5432/capstone'
