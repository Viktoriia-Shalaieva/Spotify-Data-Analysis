import logging
import os


# Ensure the 'logs' directory exists
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Log format with timestamp, level, and message
    datefmt='%d-%b-%y %H:%M:%S', # Date format for the timestamp
    handlers=[
        # Write logs to "logs/app.log" with UTF-8 encodingz
        logging.FileHandler("logs/app.log", encoding="utf-8"),
        logging.StreamHandler()  # Output logs to the console
    ]
)


# Create a named logger for the project ("spotify_project")
logger = logging.getLogger("spotify_project")
