from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, Integer

from backend.database import db


class Item(db.Model):  # type: ignore
    """Models the data of an item."""

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(180), nullable=False)
    auctions = relationship('Auction', backref='item',
                            lazy=True, cascade='all, delete-orphan')

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
            'name': self.name
        }

    def serialize_with_auctions(self):
        return {
            'id': self.id,
            'name': self.name,
            'auctions': [auction.id for auction in self.auctions]
        }

    def __repr__(self):
        return (
            f'<Item id:int:{self.id}, name:str:{self.name}, auctions:list:'
            f'{[auction.serialize() for auction in self.auctions]}>'
        )
