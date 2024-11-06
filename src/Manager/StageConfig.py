import json
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("game.log"),
        logging.StreamHandler()
    ]
)


class StageConfig:
    def __init__(self, project_root, stage):
        config_path = os.path.join(project_root, "config", "stage", f"{stage}.json")
        config_path = os.path.normpath(config_path)  # Normalize the path
        logging.info(f"Loading Stage Config from: {config_path}")

        if not os.path.exists(config_path):
            logging.error(f"Stage configuration file not found: {config_path}")
            raise FileNotFoundError(f"Stage configuration file not found: {config_path}")

        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
                logging.info(f"Stage configuration '{stage}' loaded successfully.")
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing stage configuration: {e}")
            raise

    def getGridSize(self):
        if self.config.get("grid_size", 64) <= 0:
            logging.warning(f"Invalid grid_size '{self.config.get('grid_size', 64)}'. Setting to default value 64.")
            return 64
        return self.config.get("grid_size", 64)

    def getBackgroundImage(self) -> str:
        return self.config.get("background", "")

    def getPathImage(self) -> str:
        return self.config.get("path", "")

    def getWalkPath(self) -> list:
        return self.config.get("walk_path", [])

    def getWaveConfig(self) -> list:
        return self.config.get("waves", [])

    def getConfig(self):
        return self.config