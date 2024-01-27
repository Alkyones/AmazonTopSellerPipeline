import os, sys

from database import Database
from database import url_bases
from utils import *

def getCommand(args):
    if len(args) == 1:
        return False

    command = args[1]
    if command == '--help':
        getHelp()
    elif command == '--scrape':
        if len(args) == 2:
            print("No country code found hence program is closed.")
            return False
        url_base = getCountryWebsite(url_bases,countryCode=args[2])
        if not url_base: 
            print("Country code is invalid hence program is closed.")
            return False
        DB = Database(credentials)
        scrapeData(DB, credentials, url_base)
    elif command == '--info-country':
        getInfo(url_bases)
    else:
        print("No command found hence program is closed.")


# give credentials file path or initialize your database here
# example for credentials file:
# {
#     "dbUrl": "your_db_url",
#     "collectionName":"your_collection_name_if_exists",
#     "dbName": "your_db_name",
# }

credentialFile = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "../credentials")
)

credentials = getCredentials(credentialFile)
if credentials is None:
    sys.exit("No credentials found hence program is closed.")



if __name__ == "__main__":
    os.system('cls' if os.name=='nt' else 'clear')
    command = getCommand(sys.argv)
    sys.exit()




    
