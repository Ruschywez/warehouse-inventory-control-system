from entities import Goods, Remainder, Receipt, Shipment, BaseModel
from peewee import DoesNotExist
from typing import Optional, List
from datetime import date


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
        # name - уникальный ключ
        try:
            return self.model.get(self.model.name == name)
        except DoesNotExist:
            return None
    """По цене"""
    def get_by_price(self, price: float) -> List[Goods]:
        return list(self.model.select().where(self.model.price == price))
    def get_by_price_lower_then(self, price: float) -> List[Goods]:
        return list(self.model.select().where(self.model.price < price))
    def get_by_price_upper_then(self, price: float) -> List[Goods]:
        return list(self.model.select().where(self.model.price > price))
    def get_by_price_period(self, start: float, end: float) -> List[Goods]:
        return list(self.model.select().where(start <= self.model.price <= end))
class RemainderRepository:
    def __init__(self, model: Remainder):
        self.model = model
    def get_by_id(self, remainder) -> Optional[Remainder]:
        try:
            return self.model.get_by_id(remainder)
        except DoesNotExist:
            return None
    def create(self, good_id: int, amount: int) -> Optional[Remainder]:
        try:
            good = Goods.get_by_id(good_id)
            return self.model.create(good=good, amount=amount)
        except DoesNotExist:
            raise ValueError(f"Товар с id {good_id} не существует")
    def update(self, remainder: int, **kwargs) -> bool:
        query = self.model.update(**kwargs).where(self.model.remainder == remainder)
        return query.execute() > 0
    def delete(self, remainder: int) -> bool:
        query = self.model.delete().where(self.model.remainder == remainder)
        return query.execute() > 0
    """По товару"""
    def get_by_good_name(self, name: str) -> Optional[Remainder]:
        try:
            return self.model.get(self.model.good.name == name)
        except DoesNotExist:
            return None
    def get_by_good(self, good: Goods) -> Optional[Remainder]:
        try:
            return self.model.get(self.model.good == good)
        except DoesNotExist:
            return None
    """По количеству"""
    def get_by_amount(self, amount: int) -> List[Remainder]:
        return list(self.model.select().where(self.model.amount == amount))
    def get_by_amount_lower_then(self, amount: int) -> List[Remainder]:
        return list(self.model.select().where(self.model.amount < amount))
    def get_by_amount_upper_then(self, amount: int) -> List[Remainder]:
        return list(self.model.select().where(self.model.amount > amount))
    def get_by_amount_period(self, start: int, end: int) -> List[Remainder]:
        return list(self.model.select().where(start <= self.model.amount <= end))
class ReceiptRepository:
    def __init__(self, model: Receipt):
        self.model = model
    def get_by_id(self, receipt) -> Optional[Receipt]:
        try:
            return self.model.get_by_id(receipt)
        except DoesNotExist:
            return None
    def find_all(self) -> List[Receipt]:
        return list(self.model.select())
    
    """По дате"""
    def get_by_date(self, date: date) -> List[Receipt]:
        return list(self.model.select().where(self.model.date == date))
    def get_before_date(self, date: date) -> List[Receipt]:
        return list(self.model.select().where(self.model.date < date))
    def get_after_date(self, date: date) -> List[Receipt]:
        return list(self.model.select().where(self.model.date > date))
    def get_by_date_period(self, start: date, end: date) -> List[Receipt]:
        return list(self.model.select().where(start <= self.model.date <= end))
    """по товару"""
    def get_by_good(self, good: Goods) -> List[Receipt]:
        return list(self.model.select().where(self.model.good == good))
    def get_by_good_name(self, name: str) -> List[Receipt]:
        return list(self.model.select().where(self.model.good.name == name))
    """По количеству"""
    def get_by_amount(self, amount: int) -> List[Receipt]:
        return list(self.model.select().where(self.model.amount == amount))
    def get_by_amount_lower_then(self, amount: int) -> List[Receipt]:
        return list(self.model.select().where(self.model.amount < amount))
    def get_by_amount_upper_then(self, amount: int) -> List[Receipt]:
        return list(self.model.select().where(self.model.amount > amount))
    def get_by_amount_period(self, start: int, end: int) -> List[Receipt]:
        return list(self.model.select().where(start <= self.model.amount <= end))
class ShipmentRepository:
    def __init__(self, model: Shipment):
        self.model = model
    def get_by_id(self, shipment) -> Optional[Shipment]:
        try:
            return self.model.get_by_id(shipment)
        except:
            return None
    def find_all(self) -> List[Shipment]:
        return list(self.model.select())
    def create(self, good: int | Goods, amount: int) -> Optional[Shipment]:
        if amount < 0:
            raise ValueError(f"Количество должно быть больше нуля, а получено {amount}")
        with BaseModel.Meta.database.atomic():
            try:
                remainder = Remainder.select().where(Remainder.good == good).for_update().get()
            except DoesNotExist:
                if isinstance(good, int):
                    raise ValueError(f"Остаток для товара {good} не найден")
                else:
                    raise ValueError(f"Остаток для товара {good.name} не найден")
            if remainder.amount < amount:
                raise ValueError(f"Не достаточно остатков: {(remainder.amount - amount) * -1}")
            remainder.amount -= amount
            remainder.save()
            return Shipment.create(good=good, amount=amount, date=date.today())
    """По дате"""
    def get_by_date(self, date: date) -> List[Shipment]:
        return list(self.model.select().where(self.model.date == date))
    def get_before_date(self, date: date) -> List[Shipment]:
        return list(self.model.select().where(self.model.date < date))
    def get_after_date(self, date: date) -> List[Shipment]:
        return list(self.model.select().where(self.model.date > date))
    def get_by_date_period(self, start: date, end: date) -> List[Shipment]:
        return list(self.model.select().where(start <= self.model.date <= end))
    """По товару"""
    def get_by_good(self, good: Goods) -> List[Shipment]:
        return list(self.model.select().where(self.model.good == good))
    def get_by_good_name(self, name: str) -> List[Shipment]:
        return list(self.model.select().where(self.model.good.name == name))
    """По количеству"""
    def get_by_amount(self, amount: int) -> List[Shipment]:
        return list(self.model.select().where(self.model.amount == amount))
    def get_by_amount_lower_then(self, amount: int) -> List[Shipment]:
        return list(self.model.select().where(self.model.amount < amount))
    def get_by_amount_upper_then(self, amount: int) -> List[Shipment]:
        return list(self.model.select().where(self.model.amount > amount))
    def get_by_amount_period(self, start: int, end: int) -> List[Receipt]:
        return list(self.model.select().where(start <= self.model.amount <= end))