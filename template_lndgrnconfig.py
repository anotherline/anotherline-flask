import os

#rename file to lndgrnconfig.py when done

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = '[secret key here]'
DB_USERNAME = '[username here]'
DB_PASSWORD = '[password here]'
DEBUG = True
DATABASE_URL = 'postgresql://' + os.path.join(basedir, 'data.sql')
DEV_DATABASE_URL = 'postgresql://' + os.path.join(basedir, 'data-dev.sql')
TEST_DATABASE_URL = 'postgresql://' + os.path.join(basedir, 'data-test.sql')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TEST_DATABASE_URI = 'postgresql://' + DB_USERNAME + ':' \
		+ DB_PASSWORD + '@localhost/datatest'
SQLALCHEMY_DATABASE_URI = 'postgresql://' + DB_USERNAME + ':' \
		+ DB_PASSWORD + '@localhost/datadev'
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