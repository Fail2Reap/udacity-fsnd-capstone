from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String, Integer, DateTime

from backend.database import db


class Auction(db.Model):  # type: ignore
    """Models the data of a single auction."""

    __tablename__ = 'auctions'

    id = Column(Integer, primary_key=True, autoincrement=False)
    timestamp = Column(DateTime, nullable=False)
    bid = Column(Integer)
    buyout = Column(Integer)
    unit_price = Column(Integer)
    quantity = Column(Integer, nullable=False)
    time_left = Column(String(10), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'),
                     nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'bid': self.bid,
            'buyout': self.buyout,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'time_left': self.time_left,
            'item_id': self.item_id
        }

    def __repr__(self):
        return (
            f'<Auction id:int:{self.id}, timestamp:datetime:{self.timestamp}, '
            f'bid:int:{self.bid}, buyout:int:{self.buyout}, '
            f'unit_price:int:{self.unit_price}, quantity:int:{self.quantity}, '
            f'time_left:str:{self.time_left}, item_id:int:{self.item_id}>'
        )
