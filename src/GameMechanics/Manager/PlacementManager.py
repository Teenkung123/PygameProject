import logging
from typing import TYPE_CHECKING

from pygame import Vector2

from src.GameMechanics.Entities.Tower.Dispenser import Dispenser

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class PlacementManager:
    def __init__(self, gameScene: 'GameScene'):
        self.__gameScene = gameScene
        self.placedTower = {}

    def place(self, towerType: str, position: tuple[int, int]) -> bool:
        if position in self.placedTower:
            return False

        if Vector2(*position) in self.__gameScene.getStageManager().getPath().getFullPathCoordinates():
            logging.info("Cannot place tower on path.")
            return False

        tower = self.__getTower(towerType)
        if tower is None:
            return False

        tower.place(position)
        self.placedTower[position] = tower
        return True

    def __getTower(self, towerType: str) -> Dispenser | None:
        match towerType.lower():
            case 'dispenser':
                return Dispenser(self.__gameScene)
            case _:
                return None

    def tick(self, deltaTime: float):
        for tower in self.placedTower.values():
            try:
                tower.tick(deltaTime)
            except Exception as e:
                print(f"Error ticking tower: {e}")
                pass