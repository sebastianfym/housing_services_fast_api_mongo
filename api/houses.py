from typing import List

from fastapi import APIRouter, HTTPException, BackgroundTasks
from bson import ObjectId
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from api.router import router
from config import db_host, db_port, db_name
from db.db import MongoDbUi
from models import House, Apartment, WaterMeter, WaterMeterReading, Tariff, RentCalculationRequest, MonthlyCharge
from utilities import calculate_rent, custom_jsonable_encoder


@router.post("/houses/", status_code=HTTP_200_OK, response_model=House)
async def create_house(house: House) -> House:
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    house_collection = db.get_collection("houses")
    try:
        house = house.dict(by_alias=True)
        result = await house_collection.insert_one(house)
        created_house = await house_collection.find_one({"_id": result.inserted_id})
        return created_house
    finally:
        db.client.close()


@router.get("/houses/{house_id}", status_code=HTTP_200_OK, response_model=House)
async def read_house(house_id: str) -> House:
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    house_collection = db.get_collection("houses")
    apartment_collection = db.get_collection("apartments")
    try:
        house = await house_collection.find_one({"_id": ObjectId(house_id)})
        if house is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="House not found")
        apartments = []
        for apartment in house["apartments"]:
            full_apartment = await apartment_collection.find_one({"_id": apartment["_id"]})
            if full_apartment:
                apartments.append(full_apartment)

        house["apartments"] = apartments
        return house
    except Exception as e:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="House not found")
    finally:
        db.client.close()


@router.patch("/houses/{house_id}", status_code=HTTP_200_OK)
async def add_apartments_to_house(house_id: str, apartment_ids: List[str]):
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    house_collection = db.get_collection("houses")
    house = await house_collection.find_one({"_id": ObjectId(house_id)})
    if house is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="House not found")
    apartment_collection = db.get_collection("apartments")
    apartments = await apartment_collection.find({"_id": {"$in": [ObjectId(id) for id in apartment_ids]}}).to_list(
        length=len(apartment_ids))
    if len(apartments) != len(apartment_ids):
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="One or more apartments not found")
    house["apartments"].extend(apartments)
    await house_collection.update_one({"_id": ObjectId(house_id)}, {"$set": {"apartments": house["apartments"]}})
    db.client.close()
    return {"message": "Apartments added to house successfully"}


@router.get("/houses/{house_id}/monthly_charges/", status_code=HTTP_200_OK)
async def get_monthly_charges(house_id: str):
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    monthly_charges_collection = db.get_monthly_charges_collection()
    charges = await monthly_charges_collection.find({"house_id": ObjectId(house_id)}).to_list(length=None)
    charges = [custom_jsonable_encoder(charge) for charge in charges]
    return charges


@router.get("/charges/{house_id}/{month}/{year}", status_code=HTTP_200_OK, response_model=List[MonthlyCharge])
async def get_monthly_charges(house_id: str, month: int, year: int):
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    monthly_charges_collection = db.get_monthly_charges_collection()

    try:
        charges = await monthly_charges_collection.find({
            "house_id": house_id,
            "month": month,
            "year": year
        }).to_list(length=None)

        if not charges:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No charges found for the given house, month, and year")

        for charge in charges:
            charge["_id"] = str(charge["_id"])
            charge["house_id"] = str(charge["house_id"])
            charge["apartment_id"] = str(charge["apartment_id"])

        return charges

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.client.close()


@router.post("/houses/{house_id}/calculate_rent/", status_code=HTTP_200_OK)
async def start_calculate_rent(house_id: str, request_body: RentCalculationRequest, background_tasks: BackgroundTasks):
    month = request_body.month
    year = request_body.year
    background_tasks.add_task(calculate_rent, house_id, month, year)
    return {"message": "Calculation started"}