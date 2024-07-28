from pymongo import MongoClient
import datetime
from bson import ObjectId

class Feedback:
    def __init__(self, db):
        self.collection = db.feedback

    def create_feedback(self, data):
        feedback_data = {
            "url_id": data.get("url_id"),
            "client_id": data.get("client_id"),
            "is_phishing": data.get("is_phishing"),
            "feedback_date": datetime.datetime.utcnow(),
            "comment": data.get("comment", "")
        }
        return self.collection.insert_one(feedback_data).inserted_id

    def get_feedback(self, feedback_id):
        return self.collection.find_one({"_id": feedback_id})

    def update_feedback(self, feedback_id, update_data):
        return self.collection.update_one({"_id": feedback_id}, {"$set": update_data})

    def delete_feedback(self, feedback_id):
        return self.collection.delete_one({"_id": feedback_id})

# Initialize the database connection
client = MongoClient("mongodb+srv://abirseddiki:admin@cluster0.oj1c0ic.mongodb.net/")
db = client['PhishingDetectionDB']
feedback_entity = Feedback(db)
