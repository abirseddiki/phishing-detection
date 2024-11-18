from pymongo import MongoClient
import datetime
from bson import ObjectId

class ModelAudit:
    def __init__(self, db):
        self.collection = db.model_audit

    def create_model_audit(self, data):
        model_audit_data = {
            "version": data.get("version"),
            "description": data.get("description"),
            "deployed_on": datetime.datetime.utcnow()
        }
        return self.collection.insert_one(model_audit_data).inserted_id

    def get_model_audit(self, model_id):
        return self.collection.find_one({"_id": model_id})

    def update_model_audit(self, model_id, update_data):
        return self.collection.update_one({"_id": model_id}, {"$set": update_data})

    def delete_model_audit(self, model_id):
        return self.collection.delete_one({"_id": model_id})

# Initialize the database connection
client = MongoClient("mongodb+srv://abirseddiki:admin@cluster0.oj1c0ic.mongodb.net/")
db = client['PhishingDetectionDB']
model_audit_entity = ModelAudit(db)
