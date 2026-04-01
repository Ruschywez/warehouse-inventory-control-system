from peewee import AutoField, CharField, Check, DateField, DecimalField, DoesNotExist, ForeignKeyField, IntegerField, Model, Proxy, PostgresqlDatabase
from datetime import date
"""Файл с 4 основными сущностями.
    Сущности соответствуют 4 таблицам из БД:

    - Товары (Goods) /названия и цена товаров
    - Остатки (Remainder) /товары с их количеством на складе
    - Поступления (Receipt) /данные о поступлениях, включая товар, количество и дату
    - Отбытия (Shipment) /данные об убытии товаров, включая товар, количество и дату
"""
class BaseModel(Model): # Класс для подключения!
    class Meta:
        database = Proxy()
"""основные entity"""
class Goods(BaseModel):
    good = AutoField(primary_key=True, column_name="good_id")
    name = CharField(max_length=255, unique=True)
    price = DecimalField(decimal_places=2, auto_round=True)

    @property # декоратор нужен, чтобы обращаться к объекту не используя скобки, как будто это просто self переменная
    def current_remainder(self): # ф-ия считает остаток, вынесена, чтобы глаза не мозолить
        remainder = Remainder.get_or_none(good=self)
        return remainder.amount if remainder else 0 # на случай, если remainder.amount == None, то вернуть 0, чтобы не было ошибки
    
    def add_receipt(self, amount: int):
        """Транзакция на создание записи о поступлении товаров
            Принимает аргументы:
                amount: int - количество поступившего товара, больше нуля
            Если (остаток с указанным товаром существует) то:
                прибавить количество к остатку
            Иначе:
                Создать объект класса Remainder, записав в него остаток
            Создать объект класса Receipt с указанием товара, количества и сегодняшнюю дату
        """
        if amount <= 0:
                raise ValueError(f"Количество должно быть положительным. Получено: {amount}")
        with BaseModel.Meta.database.atomic(): # создание транзакции
            # Тело транзакции
            Receipt.create(good=self, amount=amount, date=date.today())
            remainder = Remainder.select().where(Remainder.good == self).for_update().first()
            if remainder is None:
                remainder = Remainder.create(good=self, amount=amount)
            else:
                remainder.amount += amount
                remainder.save()
    def add_shipment(self, amount: int):
        """транзакция на создание записи об отгрузке товара
            Принимает аргументы:
                amount: int - количество отгружаемого количества товаров, больше нуля
            Пытается найти остаток указанного товара:
                В случае неудачи вызвать ошибку.
            Создать запись об убытии, объект класса Shipment, записав
            количество, товар и сегодняшнюю дату

            Вычесть из остатка товаров указанное количество
        """
        if amount <= 0:
            raise ValueError(f"Количество должно быть положительным. Получено: {amount}")
        with BaseModel.Meta.database.atomic():
            # Тело транзакции
            try:
                remainder = Remainder.select().where(Remainder.good == self).for_update().get()
            except DoesNotExist:
                raise ValueError(f"Остаток для товара {self.name} не найден")
            if remainder.amount < amount:
                raise ValueError(f"Не достаточно остатков: {remainder.amount}, requested: {amount}")
            Shipment.create(good=self, amount=amount, date=date.today())
            remainder.amount -= amount
            remainder.save()
            
class Remainder(BaseModel):
    remainder = AutoField(primary_key=True, column_name="remainder_id")
    good = ForeignKeyField(Goods, backref='remainders', on_delete='CASCADE', on_update='CASCADE')
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
class Receipt(BaseModel):
    receipt = AutoField(primary_key=True, column_name="receipt_id")
    good = ForeignKeyField(Goods, backref='receipts', on_delete='CASCADE', on_update='CASCADE')
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
    date = DateField()
class Shipment(BaseModel):
    shipment = AutoField(primary_key=True, column_name="shipment_id")
    good = ForeignKeyField(Goods, backref='shipments', on_delete='CASCADE', on_update='CASCADE')
    amount = IntegerField(constraints=[Check('amount >= 0')], default=0)
    date = DateField()