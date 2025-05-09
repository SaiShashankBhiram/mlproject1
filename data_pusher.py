import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv
from src.MLProject1.logger import logging
from src.MLProject1.exception import CustomException

# Load environment variables
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
ca = certifi.where()

class StudentDataExtract:
    def __init__(self):
        pass

    def cv_to_json_convertor(self, file_path):
        try:
            df = pd.read_csv(file_path)
            return json.loads(df.to_json(orient="records"))  # Convert DataFrame to JSON list
        except Exception as e:
            raise CustomException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            db = mongo_client[database]
            coll = db[collection]
            coll.insert_many(records)
            return len(records)
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    FILE_PATH = "data/student_raw.csv"
    DATABASE = "SaiShashankDB"
    COLLECTION = "StudentData"

    dataobj = StudentDataExtract()
    records = dataobj.cv_to_json_convertor(FILE_PATH)
    print(records)
    no_of_records = dataobj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(f"Inserted {no_of_records} records into MongoDB")

