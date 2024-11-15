import logging
from typing import TYPE_CHECKING

from pygame import Vector2

from src.GameMechanics.Entities.Tower import Tower

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class PlacementManager:
    def __init__(self, gameScene: 'GameScene'):
        self.__gameScene = gameScene
        self.placedTower = {}

    def place(self, position: tuple[int, int]) -> bool:
        towerType = self.__gameScene.getInventoryManager().getSelectedTower()
        if position in self.placedTower:
            return False

        if position[1] == 0:
            return False

        if Vector2(*position) in self.__gameScene.getStageManager().getPath().getFullPathCoordinates():
            logging.info("Cannot place tower on path.")
            return False

        tower = self.__createTower(towerType)
        if tower is None:
            logging.error(f"Invalid tower type: {towerType}, please check tower configurations.")
            return False

        cost: int = self.__gameScene.getTowerConfig().getTowerLevelConfig(towerType, 1).get("cost")

        if self.__gameScene.getCurrencyManager().getCurrency("gold") < cost:
            self.__gameScene.getUIManager().currencyUI.setTick()
            return False

        self.__gameScene.getCurrencyManager().withdraw("gold", cost)

        tower.place(position)
        self.placedTower[position] = tower
        return True

    def __createTower(self, towerType: str) -> Tower | None:
        try:
            tower = Tower(self.__gameScene, towerType)
            return tower
        except Exception as e:
            logging.error(f"Error creating tower '{towerType}': {e}")
            return None

    def tick(self, deltaTime: float):
        for tower in self.placedTower.values():
            try:
                tower.tick(deltaTime)
            except Exception as e:
                logging.error(f"Error ticking tower: {e}")

    def draw(self):
        for tower in self.placedTower.values():
            tower.draw()
