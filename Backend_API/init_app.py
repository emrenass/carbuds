from flask import Flask, request, g, current_app, session
from Backend_API.routes.routes_user_management import route_user_management
from Backend_API.routes.routes_matchmaking import route_matchmaking
import Backend_API.utils.carbuds_config as cfg


def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'my_secret_key'

    if config == 'PROD':
        config = cfg.FlaskProductionConfig
    elif config == 'DEV':
        config = cfg.FlaskDevelopmentConfig
    else:
        config = cfg.FlaskConfig

    app.config.from_object(config)

    app.register_blueprint(route_user_management)
    app.register_blueprint(route_matchmaking)

    return app


app = create_app('DEV')

app.run(port=5000)
