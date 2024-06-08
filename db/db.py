from motor.motor_asyncio import AsyncIOMotorClient


class MongoDbUi:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def get_monthly_charges_collection(self):
        return self.db["monthly_charges"]
