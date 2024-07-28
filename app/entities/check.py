import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

class URLCheck:
    def __init__(self, db):
        self.collection = db.url_checks

    def create_check(self, data):
        check_data = {
            "url_id": ObjectId(data.get("url_id")),
            "checked_at": datetime.datetime.utcnow(),
            "result": data.get("result"),
            "model_version": data.get("model_version")
        }
        return self.collection.insert_one(check_data).inserted_id

    def get_check(self, check_id):
        return self.collection.find_one({"_id": ObjectId(check_id)})

    def update_check(self, check_id, update_data):
        return self.collection.update_one({"_id": ObjectId(check_id)}, {"$set": update_data})

    def delete_check(self, check_id):
        return self.collection.delete_one({"_id": ObjectId(check_id)})

    def get_checks_by_url(self, url_id):
        return list(self.collection.find({"url_id": ObjectId(url_id)}))

# Initialize the database connection
client = MongoClient("mongodb+srv://abirseddiki:admin@cluster0.oj1c0ic.mongodb.net/")
db = client['PhishingDetectionDB']
check_entity = URLCheck(db)
