import json
import os
import logging

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

    def getConfig(self):
        return self.config

    def getScreenWidth(self) -> int:
        return self.config.get("screen", {}).get("width", 800)

    def getScreenHeight(self) -> int:
        return self.config.get("screen", {}).get("height", 600)

    def getProjectRoot(self):
        return os.path.dirname(os.path.dirname(self.config_path))

    def getGameSettings(self, key=None):
        return self.config.get("game_settings", {}).get(key) if key else self.config.get("game_settings", {})

    def getInventory(self):
        return self.config.get("inventory", {}) if self.config.get("inventory") else {}
