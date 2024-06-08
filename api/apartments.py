from fastapi import APIRouter, HTTPException, BackgroundTasks
from bson import ObjectId
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from api.router import router
from config import db_host, db_port, db_name
from db.db import MongoDbUi
from models import Apartment, WaterMeterReading, WaterMeter


@router.post("/apartment", status_code=HTTP_200_OK, response_model=Apartment)
async def create_apartment(apartment: Apartment) -> Apartment:
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    apartment_collection = db.get_collection("apartments")
    apartment = apartment.dict(by_alias=True)
    result = await apartment_collection.insert_one(apartment)
    created_apartment = await apartment_collection.find_one({"_id": result.inserted_id})
    return created_apartment


@router.get("/apartments/{apartment_id}", status_code=HTTP_200_OK, response_model=Apartment)
async def read_apartment(apartment_id: str) -> Apartment:
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    apartment_collection = db.get_collection("apartments")
    if (apartment := await apartment_collection.find_one({"_id": ObjectId(apartment_id)})) is not None:
        return apartment
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Apartment not found")


@router.post("/apartments/{apartment_id}/water_meter", status_code=HTTP_200_OK, response_model=Apartment)
async def add_water_meter(apartment_id: str, reading: WaterMeterReading) -> Apartment:
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    apartment_collection = db.get_collection("apartments")

    apartment = await apartment_collection.find_one({"_id": ObjectId(apartment_id)})
    if not apartment:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Apartment not found")

    if not apartment.get("water_meters"):
        apartment["water_meters"] = [WaterMeter(readings=[reading]).dict(by_alias=True)]
    else:
        apartment["water_meters"][-1]["readings"].append(reading.dict(by_alias=True))

    await apartment_collection.update_one({"_id": ObjectId(apartment_id)}, {"$set": apartment})
    db.client.close()
    return apartment