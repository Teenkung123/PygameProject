import json
import logging
import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Main

class EnemyConfig:
    def __init__(self, main: 'Main'):
        self.main = main
        self.__loadEnemiesConfig()

    def __loadEnemiesConfig(self):
        enemies_config_path = os.path.join(self.main.getProjectRoot(), "config", "enemies.json")
        enemies_config_path = os.path.normpath(enemies_config_path)
        logging.info(f"Loading Enemies Config from: {enemies_config_path}")

        if not os.path.exists(enemies_config_path):
            logging.error(f"Enemies configuration file not found: {enemies_config_path}")
            sys.exit(1)

        try:
            with open(enemies_config_path, "r") as f:
                enemies_config = json.load(f)
                logging.info("Enemies configuration loaded successfully.")
                self.__config = enemies_config
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing enemies configuration: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error loading enemies configuration: {e}")
            sys.exit(1)

    def getConfig(self):
        return self.__config