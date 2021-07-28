from flask import Blueprint, jsonify

home_routes = Blueprint('home_routes', __name__)


@home_routes.get('/')
def home():
    """Home route.
    """
    return jsonify({'message': 'no place like 127.0.0.1'}), 200
