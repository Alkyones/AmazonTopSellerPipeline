from pymongo import MongoClient
import datetime
class Database:
    def __init__(self, credentials):
        self.connection = self.connectDb(credentials)

    def connectDb(self, credentials):
        try:
            db = MongoClient(credentials['connectionUrl'])
            database = db[credentials['dbName']]
            print("Connected to Mongo")
            return database
        except Exception as e:
            print(f"Failed to connect to the database: {e}")
            return None

    def insertDoc(self, collection, doc):
        try:
            col = self.connection[collection]
            date = datetime.datetime.now(tz=datetime.timezone.utc)
            doc["createdAt"] = date
            col.insert_one(doc)
            return True
        except Exception as e:
            print(f"Failed to insert document: {e}")
            return False

    def disconnectDb(self):
        try:
            if self.connection is not None:  
                self.connection.client.close()  
                print("Disconnected from the database")
                return True
            else:
                print("No active database connection to disconnect.")
                return True
        except Exception as e:
            print(f"Failed to disconnect from the database: {e}")
            return False

url_bases = {
    "au": {"country": "Australia", "url": "https://www.amazon.com.au"},
    "ae": {"country": "United Arab Emirates", "url": "https://www.amazon.ae"},
    "br": {"country": "Brazil", "url": "https://www.amazon.com.br"},
    "ca": {"country": "Canada", "url": "https://www.amazon.ca"},
    "cn": {"country": "China", "url": "https://www.amazon.cn"},
    "de": {"country": "Germany", "url": "https://www.amazon.de"},
    "es": {"country": "Spain", "url": "https://www.amazon.es"},
    "fr": {"country": "France", "url": "https://www.amazon.fr"},
    "in": {"country": "India", "url": "https://www.amazon.in"},
    "it": {"country": "Italy", "url": "https://www.amazon.it"},
    "jp": {"country": "Japan", "url": "https://www.amazon.co.jp"},
    "mx": {"country": "Mexico", "url": "https://www.amazon.com.mx"},
    "sg": {"country": "Singapore", "url": "https://www.amazon.sg"},
    "tr": {"country": "Turkey", "url": "https://www.amazon.com.tr"},
    "uk": {"country": "United Kingdom", "url": "https://www.amazon.co.uk"},
    "us": {"country": "United States", "url": "https://www.amazon.com"},
}