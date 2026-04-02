from entities import *
from typing import Optional
from datetime import date
"""Сделано в условиях поджимающего дедлайна, по референсу из интернета"""

class GoodsRepository:
    def __init__(self, model: Goods):
        self.model = model
    def get_by_id(self, good: int) -> Optional[Goods]:
        try:
            return self.model.get_by_id(good)
        except DoesNotExist:
            return None
    def create(self, name: str, price: float) -> Goods:
        return self.model.create(name=name, price=price)
    def update(self, good: int, **kwargs) -> bool:
        query = self.model.update(**kwargs).where(self.model.good == good)
        return query.execute() > 0
    def delete(self, good: int) -> bool:
        query = self.model.delete().where(self.model.good == good)
        return query.execute() > 0
    def get_by_name(self, name: str) -> Optional[Goods]:
        try:
            return self.model.get(self.model.name == name)
        except DoesNotExist:
            return None
class RemainderRepository:
    def __init__(self, model: Remainder):
        self.model = model
    def get_by_id(self, remainder) -> Optional[Remainder]:
        try:
            return self.model.get_by_id(remainder)
        except DoesNotExist:
            return None
    def create(self, good: int, amount: int):
        return self.model.create(good=good, amount=amount)
    def update(self, remainder: int, **kwargs) -> bool:
        query = self.model.update(**kwargs).where(self.model.remainder == remainder)
        return query.execute() > 0
    def delete(self, remainder: int) -> bool:
        query = self.model.delete().where(self.model.remainder == remainder)
        return query.execute() > 0
    def get_by_good_name(self, name: str) -> Optional[Remainder]:
        try:
            return self.model.get(self.model.good.name == name)
        except DoesNotExist:
            return None
    def get_by_good(self, good: Goods) -> Optional[Goods]:
        try:
            return self.model.get(self.model.good == good)
        except DoesNotExist:
            return None
class ReceiptRepository:
    def __init__(self, model: Receipt):
        self.model = model
    def get_by_id(self, receipt) -> Optional[Receipt]:
        try:
            return self.model.get_by_id(receipt)
        except:
            return None
    def get_by_date(self, date: date) -> Optional[Receipt]:
        try:
            return self.model.get(self.model.date == date)
        except:
            return None
    def get_by_good(self, good: Goods) -> Optional[Receipt]:
        try:
            return self.model.get(self.model.good == good)
        except DoesNotExist:
            return None
    def get_by_good_name(self, name: str) -> Optional[Receipt]:
        try:
            return self.model.get(self.model.good.name == name)
        except DoesNotExist:
            return None
    # def get_by_amount_lower_then(self, amount: int):
    #     try:
    #         return self.
class ShipmentRepository:
    def __init__(self, model: Shipment):
        self.model = model
    def get_by_id(self, shipment) -> Optional[Shipment]:
        try:
            return self.model.get_by_id(shipment)
        except:
            return None
    def get_by_date(self, date: date) -> Optional[Shipment]:
        try:
            return self.model.get(self.model.date == date)
        except:
            return None
    def get_by_good(self, good: Goods) -> Optional[Shipment]:
        try:
            return self.model.get(self.model.good == good)
        except DoesNotExist:
            return None
    def get_by_good_name(self, name: str) -> Optional[Shipment]:
        try:
            return self.model.get(self.model.good.name == name)
        except DoesNotExist:
            return None