import os

#rename file to lndgrnconfig.py when done

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '[secret key here]'
DEBUG = True
DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
DEV_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
TEST_DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
LNDGRN_ADMIN = '[admin name here]'

# email server
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = '[your email address here]'
MAIL_PASSWORD = '[your email password here]'
LNDGRN_MAIL_SUBJECT_PREFIX = '[your email subject prefix here]'
LNDGRN_MAIL_SENDER = '[your desired email sender address here]'

# administrator list
ADMINS = ['[email address of admins here]']