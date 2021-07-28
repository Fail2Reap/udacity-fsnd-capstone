import json
import unittest
from random import choice

from backend.database.models import Auction, Item
from backend import create_app, APP_ROOT
from .utils.auth import get_token


def populate_db():
    with open(f'{APP_ROOT}/test/data/items.json') as f:
        items = json.load(f)

    for item in items:
        new_item = Item(
            id=item['id'],
            name=item['name']
        )
        new_item.insert()

    with open(f'{APP_ROOT}/test/data/auctions.json') as f:
        auctions = json.load(f)

    for auction in auctions:
        new_auction = Auction(
            id=auction['id'],
            timestamp=auction['timestamp'],
            bid=auction['bid'],
            buyout=auction['buyout'],
            unit_price=auction['unit_price'],
            quantity=auction['quantity'],
            time_left=auction['time_left'],
            item_id=auction['item_id']
        )
        new_auction.insert()

    return ([item['id'] for item in items],
            [auction['id'] for auction in auctions])


def cleanup_db(self):
    items = Item.query.filter(Item.id.in_(self.items)).all()
    auctions = Auction.query.filter(Auction.id.in_(self.auctions)).all()

    for auction in auctions:
        auction.delete()

    for item in items:
        item.delete()


class PublicUserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config/testing.py')
        self.client = self.app.test_client

        with self.app.app_context():
            self.headers = {
                'Authorization': get_token('public'),
                'Content-Type': 'application/json'
            }

        self.items, self.auctions = populate_db()

    def tearDown(self):
        cleanup_db(self)

    def test_403_get_items(self):

        res = self.client().get('/items', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('items', None))

    def test_403_get_item(self):

        res = self.client().get('/item/172097', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('item', None))

    def test_403_create_item(self):

        res = self.client().post(
            '/items',
            json=dict(id=4119196, name='My Most Amazing item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('created', None))

    def test_403_update_item(self):

        item_id = choice(self.items)

        res = self.client().patch(
            f'/item/{item_id}',
            json=dict(name='Now, the coolest item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('updated', None))

    def test_403_delete_item(self):

        item = choice(Item.query.all())
        item_id = item.id

        res = self.client().delete(
            f'/item/{item_id}',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('deleted', None))

    def test_403_get_auctions(self):

        res = self.client().get('/auctions', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_403_get_auction(self):

        res = self.client().get('/auction/00114894', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('auction', None))

    def test_403_create_auction(self):

        res = self.client().post(
            '/auctions',
            json=dict(
                id=5451231,
                timestamp='2021-07-18 22:11:33.433027',
                bid=0,
                item_id=186358
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('created', None))

    def test_403_update_auction(self):

        res = self.client().patch(
            '/auction/1732042111',
            json=dict(
                time_left='LONG'
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('updated', None))

    def test_403_delete_auction(self):

        res = self.client().delete(
            '/auction/4119196',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('deleted', None))


class FreeUserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config/testing.py')
        self.client = self.app.test_client

        with self.app.app_context():
            self.headers = {
                'Authorization': get_token('free'),
                'Content-Type': 'application/json'
            }

        self.items, self.auctions = populate_db()

    def tearDown(self):
        cleanup_db(self)

    def test_403_get_items(self):

        res = self.client().get('/items', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('items', None))

    def test_get_item(self):

        res = self.client().get('/item/172097', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('item', None))

    def test_404_get_item(self):

        res = self.client().get('/item/00114894', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('item', None))

    def test_403_create_item(self):

        res = self.client().post(
            '/items',
            json=dict(id=4119196, name='My Most Amazing item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('created', None))

    def test_403_update_item(self):

        item_id = choice(self.items)

        res = self.client().patch(
            f'/item/{item_id}',
            json=dict(name='Now, the coolest item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('updated', None))

    def test_403_delete_item(self):

        item = choice(Item.query.all())
        item_id = item.id

        res = self.client().delete(
            f'/item/{item_id}',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('deleted', None))

    def test_403_get_auctions(self):

        res = self.client().get('/auctions', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_get_auction(self):

        res = self.client().get('/auction/1999415', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('auction', None))

    def test_404_get_auction(self):

        res = self.client().get('/auction/00114894', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('auction', None))

    def test_403_create_auction(self):

        res = self.client().post(
            '/auctions',
            json=dict(
                id=5451231,
                timestamp='2021-07-18 22:11:33.433027',
                bid=0,
                item_id=186358
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('created', None))

    def test_403_update_auction(self):

        res = self.client().patch(
            '/auction/1732042111',
            json=dict(
                time_left='LONG'
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('updated', None))

    def test_403_delete_auction(self):

        res = self.client().delete(
            '/auction/4119196',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('deleted', None))


class PremiumUserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config/testing.py')
        self.client = self.app.test_client

        with self.app.app_context():
            self.headers = {
                'Authorization': get_token('premium'),
                'Content-Type': 'application/json'
            }

        self.items, self.auctions = populate_db()

    def tearDown(self):
        cleanup_db(self)

    def test_get_items(self):

        res = self.client().get('/items', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('items', None))

    def test_404_get_items(self):

        cleanup_db(self)

        res = self.client().get('/items', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

        populate_db()

    def test_get_item(self):

        res = self.client().get('/item/172097', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('item', None))

    def test_404_get_item(self):

        res = self.client().get('/item/00114894', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('item', None))

    def test_403_create_item(self):

        res = self.client().post(
            '/items',
            json=dict(id=4119196, name='My Most Amazing item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('created', None))

    def test_403_update_item(self):

        item_id = choice(self.items)

        res = self.client().patch(
            f'/item/{item_id}',
            json=dict(name='Now, the coolest item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('updated', None))

    def test_403_delete_item(self):

        item = choice(Item.query.all())
        item_id = item.id

        res = self.client().delete(
            f'/item/{item_id}',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('deleted', None))

    def test_get_auctions(self):

        res = self.client().get('/auctions', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('auctions', None))

    def test_404_get_auctions(self):

        cleanup_db(self)

        res = self.client().get('/auctions', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

        populate_db()

    def test_get_auction(self):

        res = self.client().get('/auction/1999415', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('auction', None))

    def test_404_get_auction(self):

        res = self.client().get('/auction/00114894', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('auction', None))

    def test_403_create_auction(self):

        res = self.client().post(
            '/auctions',
            json=dict(
                id=5451231,
                timestamp='2021-07-18 22:11:33.433027',
                bid=0,
                item_id=186358
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('created', None))

    def test_403_update_auction(self):

        res = self.client().patch(
            '/auction/1732042111',
            json=dict(
                time_left='LONG'
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('updated', None))

    def test_403_delete_auction(self):

        res = self.client().delete(
            '/auction/4119196',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('deleted', None))


class AdminUserTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config/testing.py')
        self.client = self.app.test_client

        with self.app.app_context():
            self.headers = {
                'Authorization': get_token('admin'),
                'Content-Type': 'application/json'
            }

        self.items, self.auctions = populate_db()

    def tearDown(self):
        cleanup_db(self)

    def test_get_items(self):

        res = self.client().get('/items', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('items', None))

    def test_404_get_items(self):

        cleanup_db(self)

        res = self.client().get('/items', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

        populate_db()

    def test_get_item(self):

        res = self.client().get('/item/172097', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('item', None))

    def test_404_get_item(self):

        res = self.client().get('/item/00114894', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('item', None))

    def test_create_item(self):

        res = self.client().post(
            '/items',
            json=dict(id=4119196, name='My Most Amazing item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 4119196)

    def test_400_create_item(self):

        res = self.client().post(
            '/items',
            json=dict(id='', name='My Most Amazing item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('created', None))

    def test_update_item(self):

        item_id = choice(self.items)

        res = self.client().patch(
            f'/item/{item_id}',
            json=dict(name='Now, the coolest item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data.get('updated', None), item_id)

        cleanup_db(self)
        populate_db()

    def test_404_update_item(self):

        res = self.client().patch(
            '/item/1732042111',
            json=dict(name='Now, the coolest item'),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('updated', None))

    def test_delete_item(self):

        item = choice(Item.query.all())
        item_id = item.id

        res = self.client().delete(
            f'/item/{item_id}',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data.get('deleted', None), item_id)

        cleanup_db(self)
        populate_db()

    def test_404_delete_item(self):

        res = self.client().delete(
            '/item/4119196',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('deleted', None))

    def test_get_auctions(self):

        res = self.client().get('/auctions', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('auctions', None))

    def test_404_get_auctions(self):

        cleanup_db(self)

        res = self.client().get('/auctions', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

        populate_db()

    def test_get_auction(self):

        res = self.client().get('/auction/1999415', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data.get('auction', None))

    def test_404_get_auction(self):

        res = self.client().get('/auction/00114894', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('auction', None))

    def test_create_auction(self):

        res = self.client().post(
            '/auctions',
            json=dict(
                id=123144511,
                timestamp='2021-07-18 22:11:33.433027',
                bid=0,
                buyout=123144,
                unit_price=0,
                quantity=23,
                time_left='SHORT',
                item_id=186358
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'], 123144511)

    def test_400_create_auction(self):

        res = self.client().post(
            '/auctions',
            json=dict(
                id=5451231,
                timestamp='2021-07-18 22:11:33.433027',
                bid=0,
                item_id=186358
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('created', None))

    def test_update_auction(self):

        auction_id = choice(self.auctions)

        res = self.client().patch(
            f'/auction/{auction_id}',
            json=dict(
                quantity=25,
                time_left='LONG',
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data.get('updated', None), auction_id)

        cleanup_db(self)
        populate_db()

    def test_404_update_auction(self):

        res = self.client().patch(
            '/auction/1732042111',
            json=dict(
                time_left='LONG'
            ),
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('updated', None))

    def test_delete_auction(self):

        auction = choice(Auction.query.all())
        auction_id = auction.id

        res = self.client().delete(
            f'/auction/{auction_id}',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data.get('deleted', None), auction_id)

        cleanup_db(self)
        populate_db()

    def test_404_delete_auction(self):

        res = self.client().delete(
            '/auction/4119196',
            headers=self.headers
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertIsNone(data.get('deleted', None))


if __name__ == '__main__':
    unittest.main()
