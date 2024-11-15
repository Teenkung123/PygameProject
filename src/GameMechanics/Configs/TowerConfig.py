import json
import logging
import os
import sys

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene


class TowerConfig:
    def __init__(self, gameScene: 'GameScene'):
        self.main = gameScene
        self.loadedConfigs = {}
        self.__loadTowersConfig()

    def __loadTowersConfig(self):
        towers_config_path = os.path.join(self.main.getProjectRoot(), "config", "towers")
        towers_config_path = os.path.normpath(towers_config_path)
        logging.info(f"Loading Towers Config from: {towers_config_path}")

        if not os.path.exists(towers_config_path):
            logging.error(f"Towers configuration directory not found: {towers_config_path}")
            sys.exit(1)

        for file in os.listdir(towers_config_path):
            if file.endswith(".json"):
                try:
                    with open(os.path.join(towers_config_path, file), "r") as f:
                        tower_config = json.load(f)
                        logging.info(f"Tower configuration loaded successfully: {file}")
                        self.loadedConfigs[file.replace(".json", "")] = tower_config
                except json.JSONDecodeError as e:
                    logging.error(f"Error parsing tower configuration '{file}': {e}")
                    sys.exit(1)
                except Exception as e:
                    logging.error(f"Unexpected error loading tower configuration '{file}': {e}")
                    sys.exit(1)

    def getTowerConfig(self, towerName: str) -> dict:
        return self.loadedConfigs.get(towerName)

    def getTowerLevelConfig(self, towerName: str, level: int) -> Any | None:
        tower_config = self.loadedConfigs.get(towerName)
        if tower_config:
            return tower_config.get(str(level))
        return None
