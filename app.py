from src.MLProject1.logger import logging
from src.MLProject1.exception import CustomException
from src.MLProject1.components.data_ingestion import DataIngestion
from src.MLProject1.components.data_ingestion import DataIngestionConfig
from src.MLProject1.components.data_transformation import DataTransformationConfig, DataTransformation
from src.MLProject1.components.model_trainer import ModelTrainer, ModelTrainerConfig
from dotenv import load_dotenv
import mlflow
import os
import sys
import dagshub

import sys

dagshub.init(repo_owner='SaiShashankBhiram', repo_name='mlproject1', mlflow=True)

if __name__ == "__main__":
    logging.info("The execution has started...")

    try:

        load_dotenv()

        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
        mlflow.set_experiment("Best_Model_Experiment")


        data_ingestion = DataIngestion()
        #data_ingestion_config = DataIngestionConfig()
        #data_ingestion.export_data_to_csv()
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

        #data_transformation_config = DataTransformationConfig()
        data_transformation = DataTransformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)

        model_trainer = ModelTrainer()
        print(model_trainer.initiate_model_trainer(train_arr, test_arr))
        logging.info("The model training has been completed successfully.")

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        raise CustomException(e, sys)
    



