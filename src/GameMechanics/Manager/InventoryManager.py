import json
import logging
import os.path
from typing import TYPE_CHECKING

import pygame.image

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Elements.InventoryElement import InventoryUI

class InventoryManager:
    def __init__(self, gameScene: 'GameScene', inventoryUI: 'InventoryUI'):
        self.__gameScene = gameScene
        self.__inventoryUI = inventoryUI
        self.__config = gameScene.getConfig().getInventory()
        self.__insertItem()
        self.__selectedTower = "dispenser"
        pass

    def __insertItem(self):
        for item in self.__config['slots']:
            slot: int = int(item)
            path = os.path.join(self.__gameScene.getProjectRoot(), "config", "towers", self.__config['slots'][item]+".json")
            tower_path = os.path.normpath(path)
            if not os.path.exists(tower_path):
                logging.error(f"InventoryManager tower not found: {tower_path}")
                raise FileNotFoundError(f"InventoryManager tower not found: {tower_path}")
            with open(tower_path) as f:
                try:
                    data = json.load(f)
                    ipath = os.path.join(self.__gameScene.getProjectRoot(), data['image'])
                    image_path = os.path.normpath(ipath)
                    img = pygame.image.load(image_path)
                    img = pygame.transform.scale(img, (self.__gameScene.getStageManager().getStageConfig().getGridSize() * 0.8, self.__gameScene.getStageManager().getStageConfig().getGridSize() * 0.8))

                    self.__inventoryUI.setSlot(slot, {"image": img, "name": self.__config['slots'][item]})
                except Exception as e:
                    logging.error(f"Error inserting item into inventory: {e}")

    def setSelectedTower(self, towerName: str):
        self.__selectedTower = towerName

    def getSelectedTower(self):
        return self.__selectedTower