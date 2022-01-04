import pymongo


client = pymongo.MongoClient(
    "mongodb+srv://markosaris:markosaris@cluster0.rmljq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('farmers_buddy_db')


db.users.insert_one({"username": "markos"})
