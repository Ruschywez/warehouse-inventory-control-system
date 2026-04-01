from src import *

db = create_db_connect()
BaseModel._meta.database.initialize(db)
db.connect()

# Проверяем, есть ли таблицы
tables = db.get_tables()
print(f"Существующие таблицы: {tables}")

# Теперь работаем
goods_list = list(Goods.select())
print(goods_list)

db.close()