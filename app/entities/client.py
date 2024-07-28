# client.py
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

class Client:
    def __init__(self, db):
        self.collection = db.clients

    def create(self, data):
        client_data = {
            "name": data.get("name"),
            "contact_email": data.get("contact_email"),
            "created_at": datetime.datetime.utcnow(),
            "active": data.get("active", True)
        }
        return self.collection.insert_one(client_data).inserted_id

    def get_client(self, client_id):
        return self.collection.find_one({"_id": ObjectId(client_id)})

    def update_client(self, client_id, update_data):
        return self.collection.update_one({"_id": ObjectId(client_id)}, {"$set": update_data})

    def deactivate_client(self, client_id):
        return self.update_client(client_id, {"active": False})

# Initialize the database connection
client = MongoClient("mongodb+srv://abirseddiki:admin@cluster0.oj1c0ic.mongodb.net/")
db = client['PhishingDetectionDB']
client_entity = Client(db)
