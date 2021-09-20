import pymongo 
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://admin:<password>@cluster0.r4to4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
## database name: sldb, collection name: inventory
db = cluster.sldb                      # db = cluster["sldb"]
collection = db.inventory              # collection = db["inventory"]
dbs = cluster.list_database_names()    # get a list of the names of all databases on the connected server
print(dbs)

#### MongoDB CRUD Operations

### Insert Documents
inventory = [
    {"item": "journal",
     "qty": 25,
     "size": {"h": 14, "w": 21, "uom": "cm"},
     "status": "A"},
    {"item": "notebook",
     "qty": 50,
     "size": {"h": 8.5, "w": 11, "uom": "in"},
     "status": "A"},
    {"item": "paper",
     "qty": 100,
     "size": {"h": 8.5, "w": 11, "uom": "in"},
     "status": "D"},
    {"item": "planner",
     "qty": 75, "size": {"h": 22.85, "w": 30, "uom": "cm"},
     "status": "D"},
    {"item": "postcard",
     "qty": 45,
     "size": {"h": 10, "w": 15.25, "uom": "cm"},
     "status": "A"}]
collection.insert_many(inventory)

### Query Documents ($gt: greater than; $lt: less than; $gte: greater than or equal; $lte: less than or equal; $ne: not equal; $in: in something; $nin: not in something)
## Select All Documents in a Collection
results = collection.find({})
for result in results:
    print(result)
## Specify Equality Condition
results = collection.find({"status": "D"})    # select from the inventory collection all documents where the status equals "D"
for result in results:
    print(result)
## Specify Conditions Using Query Operators
results = collection.find({"status": {"$in": ["A","D"]}})    # retrieve all documents from the inventory collection where status equals either "A" or "D"
for result in results:
    print(result)
## Specify AND Conditions
results = collection.find({"status": "A", "qty": {"$lt": 30}})    # retrieve all documents in the inventory collection where the status equals "A" and qty is less than ($lt) 30
for result in results:
    print(result)
## Specify OR Conditions
results = collection.find({"$or": [{"status": "A"}, {"qty": {"$lt": 30}}]})    # retrieve all documents in the collection where the status equals "A" or qty is less than ($lt) 30
for result in results:
    print(result)
## Specify AND as well as OR Conditions
results = collection.find({"status": "A", "$or": [{"qty": {"$lt": 30}}, {"item": {"$regex": "^p"}}]})    # select all documents in the collection where the status equals "A" and either qty is less than ($lt) 30 or item starts with the character p
for result in results:
    print(result)

### Update Documents
collection.update_one(
    {"item": "paper"},
    {"$set": {"size.uom": "cm", "status": "P"},
     "$currentDate": {"lastModified": True}})    # update the first document where item equals "paper"
collection.update_many(
    {"qty": {"$lt": 50}},
    {"$set": {"size.uom": "in", "status": "P"},
     "$currentDate": {"lastModified": True}})    # update all the document where qty < 50
collection.replace_one(
    {"item": "paper"},
    {"item": "paper",
     "instock": [
         {"warehouse": "A", "qty": 60},
         {"warehouse": "B", "qty": 40}]})     # replace item "paper" with the second object

# ### Delete Documents
collection.delete_many({})    # delete all documents from the inventory collection
collection.delete_many({"status": "A"})    # remove all documents from the inventory collection where the status field equals "A"
collection.delete_one({"status": "P"})    # delete the first document where status is "P"