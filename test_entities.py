from src import *
from sys import exit
from typing import cast
db = create_db_connect()

BaseModel._meta.database.initialize(db)
db.connect()
#/// вывод первых записей каждой таблицы
try:
    tables = db.get_tables()
    print(f"Существующие таблицы: {tables}")
except:
    print(f"не удалось извлечь таблицы")
    exit(0)
try:
    good_first = cast(Goods, Goods.select().get())
    remainder_first = cast(Remainder, Remainder.select().get())
    receipt_first = cast(Receipt, Receipt.select().get())
    shipment_first = cast(Shipment, Shipment.select().get())
    if good_first:
        print("экземпляры Entities успешно получены")
        print(f"good: {good_first.good} {good_first.name} {good_first.price}")
        print(f"remainder: {remainder_first.remainder} {remainder_first.good.name} {remainder_first.amount}")
        print(f"receipt: {receipt_first.receipt} {receipt_first.amount} {receipt_first.date} {receipt_first.good.name}")
        print(f"shipment: {shipment_first.shipment} {shipment_first.amount} {shipment_first.date} {shipment_first.good.name}")
except Exception as e:
    print(f"При извлечении экземпляров Entities произошла ошибка: {e}")
    exit(0)


db.close()