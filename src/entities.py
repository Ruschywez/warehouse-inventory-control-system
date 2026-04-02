from peewee import AutoField, CharField, Check, DateField, DecimalField, ForeignKeyField, IntegerField, Model
from .db_connect import create_db_connect
"""Файл с 4 основными сущностями.
    Сущности соответствуют 4 таблицам из БД:

    - Товары (Goods) /названия и цена товаров
    - Остатки (Remainder) /товары с их количеством на складе
    - Поступления (Receipt) /данные о поступлениях, включая товар, количество и дату
    - Отбытия (Shipment) /данные об убытии товаров, включая товар, количество и дату
"""
class BaseModel(Model): # Класс для подключения!
    class Meta:
        database = create_db_connect()
"""основные entity"""
class Goods(BaseModel):
    """
        good - уникальный идентификатор
        name - уникальный ключ, строка
        price - цена
    """
    good = AutoField(primary_key=True, column_name="good_id")
    name = CharField(max_length=255, unique=True)
    price = DecimalField(max_digits=10, decimal_places=2, auto_round=True)
    def to_dict(self) -> dict:
        """Я столкнулся с проблемой возвращения лишних данных,
        потому написал эти методы"""
        return {
            "good": self.id,
            "name": self.name,
            "price": self.price
        }
class Remainder(BaseModel):
    """
        remainder - уникальный идентификатор
        good - уникальный ключ, ссылка на товар
        amount - int количество в остатке
    """
    remainder = AutoField(primary_key=True, column_name="remainder_id")
    good = ForeignKeyField(Goods, backref='remainders', on_delete='CASCADE', on_update='CASCADE', unique=True)
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
    def to_dict(self) -> dict:
        return {
            "remainder": self.remainder,
            "good": self.good,
            "amount": self.amount
        }
class Receipt(BaseModel):
    """
        receipt - уникальны идентификатор
        good - ссылка на товар (не уникальный)
        amount - количество
        date - дата создания
    """
    receipt = AutoField(primary_key=True, column_name="receipt_id")
    good = ForeignKeyField(Goods, backref='receipts', on_delete='CASCADE', on_update='CASCADE')
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
    date = DateField()
    def to_dict(self) -> dict:
        return {
            "receipt": self.receipt,
            "good": self.good,
            "amount": self.amount,
            "date": self.date
        }
class Shipment(BaseModel):
    """
        shipment - уникальны идентификатор
        good - ссылка на товар (не уникальный)
        amount - количество
        date - дата создания
    """
    shipment = AutoField(primary_key=True, column_name="shipment_id")
    good = ForeignKeyField(Goods, backref='shipments', on_delete='CASCADE', on_update='CASCADE')
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
    date = DateField()
    def to_dict(self) -> dict:
        return {
            "shipment": self.shipment,
            "good": self.good,
            "amount": self.amount,
            "date": self.date
        }