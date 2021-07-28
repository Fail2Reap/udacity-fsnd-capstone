from typing import Any

from flask import Blueprint, jsonify, abort, request
from sqlalchemy import exc

from backend.services.auth import requires_auth
from backend.database.models import Auction, Item

auction_routes = Blueprint('auction_routes', __name__)


@auction_routes.get('/auctions')
@requires_auth('get:auctions')
def get_auctions(jwt: str):
    """Gets all auctions.
    """

    try:
        auctions = Auction.query.all()

        if not auctions:
            abort(404)

        return jsonify({
            'success': True,
            'auctions': [auction.serialize() for auction in auctions]
        }), 200

    except exc.DBAPIError:
        abort(400)


@auction_routes.post('/auctions')
@requires_auth('post:auctions')
def create_auction(jwt: str):
    """Creates a new auction.

    Args:
        id (int): Auction id.
        timestamp (datetime): datetime timestamp.
        bid (int): Auction bid amount.
        buyout (int): Auction buyout amount.
        unit_price (int): Auction unit price.
        quantity (int): Number of items.
        time_left (str): Time left on the auction.
        item_id (int): Id of the item being sold.
    """
    data: Any = request.get_json()

    try:
        item_id = data.get('item_id', None)
        time_left = data.get('time_left', None)

        if item_id:
            item = Item.query.filter(Item.id == item_id).one_or_none()

            if not item:
                return jsonify({
                    'success': False,
                    'message': (f"Item with id '{item_id}' does not exist. "
                                "Please create it first.")
                }), 400

        allowed_time_left = ['SHORT', 'MEDIUM', 'LONG', 'VERY_LONG']

        if time_left and \
           time_left.upper() not in allowed_time_left:
            return jsonify({
                'success': False,
                'message': (f"'{time_left}' is invalid. Please "
                            "specify one of the following: "
                            f"{', '.join(allowed_time_left)}")
            }), 400
        elif not time_left:
            abort(400)

        auction = Auction(
            id=data.get('id'),
            timestamp=data.get('timestamp'),
            bid=data.get('bid'),
            buyout=data.get('buyout'),
            unit_price=data.get('unit_price'),
            quantity=data.get('quantity'),
            time_left=time_left.upper(),
            item_id=item_id
        )

        auction.insert()

        return jsonify({
            'success': True,
            'created': auction.id
        })

    except exc.DBAPIError:
        abort(400)


@auction_routes.get('/auction/<int:id>')
@requires_auth('get:auction')
def get_auction(jwt: str, id: int):
    """Gets a specific auction.

    Args:
        id (int): Auction id.
    """

    try:
        auction = Auction.query.filter(Auction.id == id).one_or_none()

        if not auction:
            abort(404)

        return jsonify({
            'success': True,
            'auction': auction.serialize()
        })

    except exc.DBAPIError:
        abort(400)


@auction_routes.patch('/auction/<int:id>')
@requires_auth('patch:auction')
def update_auction(jwt: str, id: int):
    """Updates an existing auction.

    Args:
        id (int): Auction id.
        timestamp (datetime): datetime timestamp.
        bid (int): Auction bid amount.
        buyout (int): Auction buyout amount.
        unit_price (int): Auction unit price.
        quantity (int): Number of items.
        time_left (str): Time left on the auction.
        item_id (int): Id of the item being sold.
    """
    data: Any = request.get_json()

    timestamp = data.get('timestamp')
    bid = data.get('bid')
    buyout = data.get('buyout')
    unit_price = data.get('unit_price')
    quantity = data.get('quantity')
    time_left = data.get('time_left')
    item_id = data.get('item_id')

    try:
        auction = Auction.query.filter(Auction.id == id).one_or_none()

        if not auction:
            abort(404)

        if timestamp:
            auction.timestamp = timestamp

        if bid:
            auction.bid = bid

        if buyout:
            auction.buyout = buyout

        if unit_price:
            auction.unit_price = unit_price

        if quantity:
            auction.quantity = quantity

        if time_left:
            auction.time_left = time_left

        if item_id:
            item = Item.query.filter(Item.id == item_id).one_or_none()

            if not item:
                return jsonify({
                    'success': False,
                    'message': (f"'item_id' {item_id} does not exist. Please"
                                "create it first.")
                }), 400

            item.item_id = item_id

        auction.update()

        return jsonify({
            'success': True,
            'updated': auction.id
        })

    except exc.DBAPIError:
        abort(400)


@auction_routes.delete('/auction/<int:id>')
@requires_auth('delete:auction')
def delete_auction(jwt: str, id: int):
    """Deletes a specific auction.

    Args:
        id (int): Auction id.
    """
    try:
        auction = Auction.query.filter(Auction.id == id).one_or_none()

        if not auction:
            abort(404)

        auction.delete()

        return jsonify({
            'success': True,
            'deleted': id
        })

    except exc.DBAPIError:
        abort(400)
