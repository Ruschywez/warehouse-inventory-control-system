from .db_connect import db_connect
from peewee import AutoField, CharField, Check, DateField, DecimalField, ForeignKeyField, IntegerField, Model, Value
from peewee import CASCADE

"""Файл с 4 основными сущностями.
    Сущности соответствуют 4 таблицам из БД:

    - Товары (Goods) /названия и цена товаров
    - Остатки (Remainder) /товары с их количеством на складе
    - Поступления (Receipt) /данные о поступлениях, включая товар, количество и дату
    - Отбытия (Shipment) /данные об убытии товаров, включая товар, количество и дату
"""
class BaseModel(Model): # Класс для подключения!
    class Meta:
        database = db_connect()
"""основные entity"""
class Goods(BaseModel):
    good = AutoField(primary_key=True)
    name = CharField(max_length=255, unique=True)
    price = DecimalField(decimal_places=2, auto_round=True)
    def add_receipt(self, amount, date):
        with BaseModel.Meta.database.atomic(): # создание транзакции
            Receipt.create(good=self, amount=amount, date=date)
            remainder, _ = Remainder.get_or_create(good=self, defaults={'amount': 0})
            remainder.amount += amount
            remainder.save()
    def add_shipment(self, amount, date):
        with BaseModel.Meta.database.atomic():
            try:
                remainder, _ = Remainder.get(good=self)
            except Exception as e:
                raise ValueError(e)
            if remainder.amount < amount:
                raise ValueError(f"Не достаточно остатков: {remainder.amoint}, requested: {amount}")
            Shipment.create(good=self, amount=amount, date=date)
            remainder.amount -= amount
            remainder.save()
            
class Remainder(BaseModel):
    remainder_id = AutoField(primary_key=True)
    good = ForeignKeyField(Goods, backref='remainders', on_delete=CASCADE, on_update=CASCADE)
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
class Receipt(BaseModel):
    receipt_id = AutoField(primary_key=True)
    good = ForeignKeyField(Goods, backref='receipts', on_delete=CASCADE, on_update=CASCADE)
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
    date = DateField()
class Shipment(BaseModel):
    shipment_id = AutoField(primary_key=True)
    good = ForeignKeyField(Goods, backref='shipments', on_delete=CASCADE, on_update=CASCADE)
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
    date = DateField()