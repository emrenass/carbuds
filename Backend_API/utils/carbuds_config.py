from Backend_API.database import database_config

class FlaskConfig(object):
    DEBUG = False
    TESTING = False
    BABEL_DEFAULT_LOCALE = "en"
    SEND_FILE_MAX_AGE_DEFAULT = 0


class FlaskProductionConfig(FlaskConfig):

    SECRET_KEY = "FA848613990667D31E2875021B945130E4A37EDED8035E83EC2426C3366737B2"

    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_PROTECTION = 'strong'
    SESSION_COOKIE_HTTPONLY = True


    LANGUAGES = {
        'en': 'English'
    }

    DB_HOST = database_config.DB_HOST
    DB_PORT = database_config.DB_PORT
    DB_NAME = database_config.DB_NAME
    DB_USERNAME = database_config.DB_USERNAME
    DB_PASS = database_config.DB_PASS

    STATIC_FILE = "static"

    HOST = '0.0.0.0'
    PORT = '5090'

    SSL_CERT = 'certificates/test.com.crt'
    SSL_KEY = 'certificates/test.com.key'

    DIRECTIONS_API_KEY = 'AIzaSyBhWJgRmMZum5qBnjGA7HoaY_vpmyzMxe0'

    SECURE = True
    HTTPONLY = True


class FlaskDevelopmentConfig(FlaskConfig):
    DEBUG = True
    TESTING = True

    SECRET_KEY = "FA848613990667D31E2875021B945130E4A37EDED8035E83EC2426C3366737B2"

    DB_HOST = database_config.DB_HOST
    DB_PORT = database_config.DB_PORT
    DB_NAME = database_config.DB_NAME
    DB_USERNAME = database_config.DB_USERNAME
    DB_PASS = database_config.DB_PASS

    STATIC_FILE = "static"

    HOST = 'localhost'
    PORT = '5090'

    SSL_CERT = 'certificates/test.com.crt'
    SSL_KEY = 'certificates/test.com.key'

    DIRECTIONS_API_KEY = 'AIzaSyBhWJgRmMZum5qBnjGA7HoaY_vpmyzMxe0'

    SECURE = False
    HTTPONLY = False




