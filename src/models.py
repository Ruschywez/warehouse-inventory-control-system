from .repositories import GoodsRepository, RemainderRepository, ReceiptRepository, ShipmentRepository
from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping() -> bool:
    return True
"""Goods - товары"""
@app.get("/goods")
def list_goods():
    return {"goods": GoodsRepository.find_all()}
@app.get("/goods/{good_id}")
def get_good(good_id: int):
    return {"good": GoodsRepository.get_by_id(good_id)}