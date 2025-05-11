import os
import sys
import pandas as pd
import pymongo
from dotenv import load_dotenv
from src.MLProject1.exception import CustomException
from src.MLProject1.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import numpy as np

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

def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)
