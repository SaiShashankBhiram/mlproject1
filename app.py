from src.MLProject1.logger import logging
from src.MLProject1.exception import CustomException
from src.MLProject1.components.data_ingestion import DataIngestion
from src.MLProject1.components.data_ingestion import DataIngestionConfig
from src.MLProject1.components.data_transformation import DataTransformationConfig, DataTransformation

import sys

if __name__ == "__main__":
    logging.info("The execution has started...")

    try:
        data_ingestion = DataIngestion()
        #data_ingestion_config = DataIngestionConfig()
        #data_ingestion.export_data_to_csv()
        train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()

        #data_transformation_config = DataTransformationConfig()
        data_transformation = DataTransformation()
        data_transformation.initiate_data_transformation(train_data_path, test_data_path)

    except Exception as e:
        logging.error("An error occurred: %s", str(e))
        raise CustomException(e, sys)


