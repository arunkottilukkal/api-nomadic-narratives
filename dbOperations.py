from pymongo import MongoClient

class Database:
    def __init__(self):
        self.secret_key = "mongodb://db-nomadic-narratives:1NxeiGCq6NOzcTVHi1gld70OSe6NtF1zv6F0wTweJjI8X0f6e93gEQ5QPyxReseBcnCe0fMDoAkTACDbY9HuQw==@db-nomadic-narratives.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@db-nomadic-narratives@"
        self.db_name = "db-nomadic-narratives"
    
    def initConnection(self):
        self.client = MongoClient(self.secret_key)
        self.db = self.client.get_database(self.db_name)
    
    def getAllCollections(self):
        return self.db.list_collection_names()

    def insertData(self, collectionName:str="", payload:list=[]):
        self.collection = self.db[collectionName]
        records = self.collection.insert_many(payload)
        return len(records.inserted_ids)

    def fetchData(self, collectionName:str="", condition:dict={}):
        self.collection = self.db[collectionName]
        return self.collection.find(condition)


        
        