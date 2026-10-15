import logging
import os
from datetime import datetime
from pathlib import Path

# 1. Create a clean file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Define the directory path (ONLY up to the "logs" folder)
# logs_path = os.path.join(os.getcwd(), "logs")
root_path=Path(__file__).resolve().parent.parent
logs_path=root_path/"logs"

# 3. Create the "logs" folder if it doesn't exist
# os.makedirs(logs_path, exist_ok=True)
logs_path.mkdir(parents=True,exist_ok=True)

# 4. Correctly join the logs folder with the log file name
# LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
LOG_FILE_PATH = logs_path/LOG_FILE

# 5. Initialize logger setup
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if __name__=="__main__":
    logging.info("Logging has started")

