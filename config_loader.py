# config_loader.py

import json
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("game.log"),
        logging.StreamHandler()
    ]
)

class ConfigLoader:
    def __init__(self, config_path="config/config.json"):
        self.config_path = os.path.normpath(config_path)
        self.config = self.__load_config()

    def __load_config(self):
        if not os.path.exists(self.config_path):
            logging.error(f"Configuration file not found: {self.config_path}")
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                logging.info(f"Loaded configuration from {self.config_path}")
                return config
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing configuration file: {e}")
            raise

    def get_config(self):
        return self.config
