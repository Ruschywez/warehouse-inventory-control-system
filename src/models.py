from .repositories import GoodsRepository, RemainderRepository, ReceiptRepository, ShipmentRepository
from .entities import Goods, Remainder, Receipt, Shipment
from fastapi import FastAPI, Query, HTTPException, status
from decimal import Decimal
from typing import Optional

goodsRepository = GoodsRepository(Goods())
remainderRepository = RemainderRepository(Remainder())
receiptRepository = ReceiptRepository(Receipt())
shipmentRepository = ShipmentRepository(Shipment())

app = FastAPI()

@app.get("/ping") # проверка подключения
def ping() -> bool:
    return True

"""Goods - товары"""
@app.get("/goods/")
def get_good(good_id: int = Query(None, ge=0)):
    if good_id is not None:
        good = goodsRepository.get_by_id(good_id)
        if good is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Good not found")
        return {"good": goodsRepository.get_by_id(good_id).to_dict()}
    else:
        return {"goods": [good.to_dict() for good in goodsRepository.find_all()]}
    
@app.post("/goods/")
def create_good(
        name: str = Query(..., min_length=2, max_length=255),
        price: Decimal = Query(..., ge=0.0, le=99_999_999.99)
    ):
    return {"good": goodsRepository.create(name=name, price=price).to_dict()}

@app.patch("/goods/")
def patch_good(
        good: int,
        name: Optional[str] = Query(None, min_length=1, max_length=255),
        price: Optional[Decimal] = Query(None, ge=0, le=99_999_999.99)
    ):
    """Нейронка ревъюер предложила следующий вариант, но мне трудно его прочесть,
    потому пока отказзался в пользу простого
        # Фильтруем None значения (не переданные параметры)
        update_data = {k: v for k, v in {
            "name": name,
            "price": price
        }.items() if v is not None}
    """
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if price is not None:
        update_data["price"] = price
    
    if not update_data: # ошибка на случай, если никакие данные не получены
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields to update")
    success = goodsRepository.update(good=good, **update_data)
    if success:
        return {"message": f"Good {good} updated", "updated_fields": update_data}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Good not found")
    
@app.delete("/goods/{good_id}")
def delete_good(good_id: int):
    success = goodsRepository.delete(good_id)
    if success:
        return {"message": f"Good {good_id} success deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Good not found")