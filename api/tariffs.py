from fastapi import APIRouter, HTTPException, BackgroundTasks
from bson import ObjectId
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from api.router import router
from config import db_name, db_port, db_host
from db.db import MongoDbUi
from models import Tariff


@router.post("/tariffs/", status_code=HTTP_200_OK, response_model=Tariff)
async def create_tariff(tariff: Tariff) -> Tariff:
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    tariff_collection = db.get_collection("tariffs")
    tariff = tariff.dict(by_alias=True)
    result = await tariff_collection.insert_one(tariff)
    created_tariff = await tariff_collection.find_one({"_id": result.inserted_id})
    return created_tariff


@router.get("/tariffs/{tariff_id}", status_code=HTTP_200_OK, response_model=Tariff)
async def read_tariff(tariff_id: str) -> Tariff:
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    tariff_collection = db.get_collection("tariffs")
    if (tariff := await tariff_collection.find_one({"_id": ObjectId(tariff_id)})) is not None:
        return tariff
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tariff not found")