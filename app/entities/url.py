from pymongo import MongoClient
from bson.objectid import ObjectId

class URL:
    def __init__(self, db):
        self.collection = db.client_urls

    def add_url(self, client_id, url):
        url_data = {
            "client_id": client_id,
            "url": url,
            "last_checked": None,
            "is_phishing": None
        }
        return self.collection.insert_one(url_data).inserted_id

    def update_url(self, url_id, update_data):
        return self.collection.update_one({"_id": ObjectId(url_id)}, {"$set": update_data})

    def get_url(self, url_id):
        return self.collection.find_one({"_id": ObjectId(url_id)})

    def get_urls_by_client(self, client_id):
        return list(self.collection.find({"client_id": client_id}))

    def delete_url(self, url_id):
        return self.collection.delete_one({"_id": ObjectId(url_id)})

# Initialize the database connection
client = MongoClient("mongodb+srv://abirseddiki:admin@cluster0.oj1c0ic.mongodb.net/")
db = client['PhishingDetectionDB']
url_entity = URL(db)
