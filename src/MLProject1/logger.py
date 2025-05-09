import logging 
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # Log file name with timestamp
log_path = os.path.join(os.getcwd(), "logs", LOG_FILE) # Path to save the log file
os.makedirs(os.path.dirname(log_path), exist_ok=True) # Create directory if it doesn't exist

LOG_FILE_PATH = log_path # Full path to the log file

logging.basicConfig(
    filename=LOG_FILE_PATH, # Log file path
    format='[%(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s', # Log message format
    level=logging.INFO # Log level
)