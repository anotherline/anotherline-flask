import os
import lndgrnconfig as settings

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

	SECRET_KEY = settings.SECRET_KEY
	DEV_DATABASE_URL = settings.DEV_DATABASE_URL
	TEST_DATABASE_URL = settings.TEST_DATABASE_URL
	DATABASE_URL = settings.DATABASE_URL
	SQLALCHEMY_COMMIT_ON_TEARDOWN = settings.SQLALCHEMY_COMMIT_ON_TEARDOWN
	LNDGRN_ADMIN = settings.LNDGRN_ADMIN

	MAIL_SERVER = settings.MAIL_SERVER
	MAIL_PORT = settings.MAIL_PORT
	MAIL_USE_TLS = settings.MAIL_USE_TLS
	MAIL_USERNAME = settings.MAIL_USERNAME
	MAIL_PASSWORD = settings.MAIL_PASSWORD
	LNDGRN_MAIL_SUBJECT_PREFIX = settings.LNDGRN_MAIL_SUBJECT_PREFIX
	LNDGRN_MAIL_SENDER = settings.LNDGRN_MAIL_SENDER

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'postgresql://' + os.path.join(basedir, 'data-dev.sql')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'postgresql://' + os.path.join(basedir, 'data-test.sql')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'postgresql://' + os.path.join(basedir, 'data.sql')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}
