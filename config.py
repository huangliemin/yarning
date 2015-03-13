# -*- coding: UTF-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'my son is huangzheyan'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	MAIL_SERVER = 'smpt.aliyun.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USE_SSL = False
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	YARNING_MAIL_SUBJECT_PREFIX = '[YARNING]'
	YARNING_MAIL_SENDER = 'Yarning Admin <fengyu19832002@aliyun.com>'
	YARNING_ADMIN = os.environ.get('YARNING_ADMIN')


	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class TestingConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}

