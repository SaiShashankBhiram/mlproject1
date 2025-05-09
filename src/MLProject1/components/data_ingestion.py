import os
import sys
from src.MLProject1.exception import CustomException
from src.MLProject1.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split

import pymongo
from dotenv import load_dotenv

from dataclasses import dataclass

load_dotenv()

@dataclass
class DataIngestionConfig:
    mongo_db_url: str = os.getenv("MONGO_DB_URL")
    database_name: str = "SaiShashankDB"
    collection_name: str = "StudentData"
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")


class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()
        self.client = pymongo.MongoClient(self.config.mongo_db_url)
        self.database = self.client[self.config.database_name]
        self.collection = self.database[self.config.collection_name]

    def export_data_to_csv(self):
        try:
            # Fetch data from MongoDB
            data = list(self.collection.find())
            if not data:
                raise CustomException("No data found in the MongoDB collection.")

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Drop the '_id' column if it exists
            if '_id' in df.columns:
                df.drop(columns=['_id'], inplace=True)

            os.makedirs(os.path.dirname(self.config.raw_data_path), exist_ok=True)

            # Save to CSV
            df.to_csv(self.config.raw_data_path, index=False, header=True)
            logging.info(f"Data exported to {self.config.raw_data_path}")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.config.train_data_path, index=False, header=True)
            test_set.to_csv(self.config.test_data_path, index=False, header=True)
            logging.info(f"Data exported to {self.config.train_data_path} and {self.config.test_data_path}")
            
            return(
                self.config.train_data_path,
                self.config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    data_ingestion = DataIngestion()
    data = data_ingestion.export_data_to_csv()
    print(data.head())