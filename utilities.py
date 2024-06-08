from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from db.db import MongoDbUi


def custom_jsonable_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return jsonable_encoder(obj)


async def calculate_rent(house_id: str, month: int, year: int):
    db = MongoDbUi(f"mongodb://{db_host}:{db_port}", f"{db_name}")
    house_collection = db.get_collection("houses")
    tariff_collection = db.get_collection("tariffs")
    apartment_collection = db.get_collection("apartments")
    monthly_charges_collection = db.get_monthly_charges_collection()

    house = await house_collection.find_one({"_id": ObjectId(house_id)})
    water_tariff = await tariff_collection.find_one({"name": "water"})
    maintenance_tariff = await tariff_collection.find_one({"name": "maintenance"})

    if house is None:
        raise HTTPException(status_code=404, detail="House not found")

    if not water_tariff or not maintenance_tariff:
        raise HTTPException(status_code=404, detail="Required tariffs not found")

    for apartment_ref in house["apartments"]:
        apartment = await apartment_collection.find_one({"_id": apartment_ref["_id"]})
        if not apartment:
            continue

        apartment_id = str(apartment["_id"])
        apartment_area = apartment["area"]
        water_meters = apartment.get("water_meters", [])
        total_water_charge = 0
        for meter in water_meters:
            readings = meter["readings"]
            current_month_reading = next(
                (r for r in readings if r["date"].month == month and r["date"].year == year), None)
            previous_month_reading = next(
                (r for r in readings if r["date"].month == month - 1 and r["date"].year == year), None)

            if current_month_reading and previous_month_reading:
                consumption = current_month_reading["value"] - previous_month_reading["value"]
                total_water_charge += consumption * water_tariff["rate"]

        maintenance_charge = apartment_area * maintenance_tariff["rate"]
        total_charge = total_water_charge + maintenance_charge

        await monthly_charges_collection.insert_one({
            "house_id": house_id,
            "apartment_id": apartment_id,
            "month": month,
            "year": year,
            "total_water_charge": total_water_charge,
            "maintenance_charge": maintenance_charge,
            "total_charge": total_charge,
            "status": "completed"
        })

    db.client.close()