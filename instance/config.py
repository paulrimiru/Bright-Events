# config.py

import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = 'secret'
    TESTING = False
class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing"""
    DEBUG = True
class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'configobj':Config,
    'SECRET_KEY':'secret_key'
}
