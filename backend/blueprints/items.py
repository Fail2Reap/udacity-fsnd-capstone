from typing import Any

from flask import Blueprint, jsonify, abort, request
from sqlalchemy import exc

from backend.services.auth import requires_auth
from backend.database.models import Item

item_routes = Blueprint('item_routes', __name__)


@item_routes.get('/items')
@requires_auth('get:items')
def get_items(jwt: str):
    """Gets all items.
    """
    try:
        items = Item.query.all()

        if not items:
            abort(404)

        return jsonify({
            'success': True,
            'items': [item.serialize() for item in items]
        }), 200

    except exc.DBAPIError:
        abort(400)


@item_routes.post('/items')
@requires_auth('post:items')
def create_item(jwt: str):
    """Creates a new item.

    Args:
        id (int): Item id.
        name (str): Item name.
    """
    data: Any = request.get_json()

    try:
        item = Item(
            id=data.get('id'),
            name=data.get('name')
        )

        item.insert()

        return jsonify({
            'success': True,
            'created': item.id
        })

    except exc.DBAPIError:
        abort(400)


@item_routes.get('/item/<int:id>')
@requires_auth('get:item')
def get_item(jwt: str, id: int):
    """Gets a specific item.

    Args:
        id (int): Item id.
    """
    try:
        item = Item.query.filter(Item.id == id).one_or_none()

        if not item:
            abort(404)

        return jsonify({
            'success': True,
            'item': item.serialize()
        })

    except exc.DBAPIError:
        abort(400)


@item_routes.patch('/item/<int:id>')
@requires_auth('patch:item')
def update_item(jwt: str, id: int):
    """Updates a specific item.

    Args:
        name (str): Item id.
    """
    data: Any = request.get_json()

    name = data.get('name')

    try:
        item = Item.query.filter(Item.id == id).one_or_none()

        if not item:
            abort(404)

        if name:
            item.name = name

        item.update()

        return jsonify({
            'success': True,
            'updated': item.id
        })

    except exc.DBAPIError:
        abort(400)


@item_routes.delete('/item/<int:id>')
@requires_auth('delete:item')
def delete_item(jwt: str, id: int):
    """Gets a specific item.

    Args:
        id (int): Item id.
    """
    try:
        item = Item.query.filter(Item.id == id).one_or_none()

        if not item:
            abort(404)

        item.delete()

        return jsonify({
            'success': True,
            'deleted': id
        })

    except exc.DBAPIError:
        abort(400)
