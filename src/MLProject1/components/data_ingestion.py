import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.MLProject1.exception import CustomException
from src.MLProject1.logger import logging
from src.MLProject1.utils import fetch_data_from_mongo

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")
    local_data_path: str = os.path.join("notebook/data", "student_raw.csv")  # Adding local data path

class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info("Fetching data from MongoDB...")
            df = fetch_data_from_mongo()  # Get data using utils.py

            # Also load local CSV data
            logging.info(f"Loading local CSV data from {self.config.local_data_path}...")
            local_df = pd.read_csv(self.config.local_data_path)
            logging.info("Local CSV data successfully loaded.")

            # Merge MongoDB and local CSV data
            df = pd.concat([df, local_df], ignore_index=True)
            logging.info("Merged MongoDB data with local CSV data.")

            os.makedirs(os.path.dirname(self.config.raw_data_path), exist_ok=True)
            df.to_csv(self.config.raw_data_path, index=False, header=True)
            logging.info(f"Raw data saved to {self.config.raw_data_path}")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.config.train_data_path, index=False, header=True)
            test_set.to_csv(self.config.test_data_path, index=False, header=True)

            logging.info(f"Train/Test split saved at {self.config.train_data_path} and {self.config.test_data_path}")

            return self.config.train_data_path, self.config.test_data_path

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    data_ingestion = DataIngestion()
    train_path, test_path = data_ingestion.export_data_to_csv()
    print(f"Train Data Path: {train_path}\nTest Data Path: {test_path}")