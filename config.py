import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    DB_NAME = "production-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    DOC_UPLOADS = os.path.join(os.getcwd(), "ginsberg_app_uploads/uploads")
    ALLOWED_DOC_EXTENSIONS = ["XLSX", "XLS", "CSV"]

    SAMPLE_FILES = os.path.join(os.getcwd(), "app/static/samples")

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    DOC_UPLOADS = "/Users/jesseginsberg/Documents/Programming/hmi_stuff/spend_upload_app_v3/app/static/docs/uploads"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"

    SESSION_COOKIE_SECURE = False