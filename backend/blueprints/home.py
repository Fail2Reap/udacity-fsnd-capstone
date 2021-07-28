from flask import Blueprint, jsonify, redirect, url_for

home_routes = Blueprint('home_routes', __name__)


@home_routes.get('/favicon.ico')
def favicon():
    """Favicon
    """
    return redirect(url_for('static', filename='favicon.ico'))


@home_routes.get('/')
def home():
    """Home route.
    """
    return jsonify({'message': 'no place like 127.0.0.1'}), 200
