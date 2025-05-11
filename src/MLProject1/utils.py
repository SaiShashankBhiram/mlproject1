import os
import sys
import pandas as pd
import pymongo
from dotenv import load_dotenv
from src.MLProject1.exception import CustomException
from src.MLProject1.logger import logging

import pickle
from dataclasses import dataclass
load_dotenv()

# Load MongoDB connection details from environment variables
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
DATABASE_NAME = "SaiShashankDB"
COLLECTION_NAME = "StudentData"

def fetch_data_from_mongo():
    """Fetches data from MongoDB and returns it as a pandas DataFrame."""
    try:
        logging.info("Connecting to MongoDB...")
        client = pymongo.MongoClient(MONGO_DB_URL)
        database = client[DATABASE_NAME]
        collection = database[COLLECTION_NAME]

        data = list(collection.find())
        if not data:
            raise CustomException("No data found in the MongoDB collection.")

        df = pd.DataFrame(data)

        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)

        logging.info("Data successfully fetched from MongoDB.")
        return df

    except Exception as e:
        raise CustomException(e, sys)
    
def save_object(obj, file_path):
    """Saves a Python object to a file using pickle."""
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
            
    except Exception as e:
        raise CustomException(e, sys)

