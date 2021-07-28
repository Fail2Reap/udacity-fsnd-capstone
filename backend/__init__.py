import os
import inspect
from pathlib import Path

from flask import Flask
from flask.blueprints import Blueprint
from flask.globals import request
from flask.json import jsonify
from flask_migrate import Migrate


from backend import blueprints
from backend.database import setup_db, reset_db, db
from backend.services.auth import AuthError


APP_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parents[0]


def create_app(test_config=None):
    """App factory for Flask applications.

    Args:
        test_config (str, optional): Path to the .py configuration file.
        Defaults to None.

    Returns:
        Flask: A Flask app.
    """

    # Creating app and configuring
    app = Flask(__name__)
    app.config.from_pyfile(
        'config/production.py' if not test_config else test_config
    )

    # Registering blueprints
    route_blueprints = [
        bp[1] for bp in inspect.getmembers(blueprints)
        if isinstance(bp[1], Blueprint)
    ]

    for blueprint in route_blueprints:
        app.register_blueprint(blueprint)

    # Setting up db and migrations
    setup_db(app)

    if app.config['TESTING']:
        reset_db()

    migrate = Migrate()
    migrate.init_app(app, db)

    # Baseline error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': {
                'code': 'bad_request',
                'description': 'The server could not understand the '
                'request due to invalid syntax.'
            }
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': {
                'code': 'unauthorized',
                'description': 'You must authenticate yourself to access '
                'this resource.'
            }
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': {
                'code': 'forbidden',
                'description': 'You do not have access to this resource.'
            }
        }), 403

    @app.errorhandler(404)
    @app.errorhandler(405)
    def _handle_api_errors(error):
        if request.path.startswith('/'):
            return jsonify({
                'success': False,
                'error': error.code,
                'message': {
                    'code': error.name.lower().replace(' ', '_'),
                    'description': "The requested URL or resource "
                                   "was not found."
                }
            }), error.code
        return error

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': {
                'code': 'unprocessable_entity',
                'description': 'The request was well-formed but was unable '
                'to be followed due to semantic errors.'
            }
        }), 422

    @app.errorhandler(AuthError)
    def _handle_auth_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code

    return app
