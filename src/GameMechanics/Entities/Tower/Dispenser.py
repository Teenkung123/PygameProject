import logging
import pygame

from src.GameMechanics.Entities.Tower.Tower import Tower
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Entities.Enemy import Enemy

class Dispenser(Tower):
    def _getConfigFileName(self):
        return "dispenser.json"

    def _applyEffect(self, enemy: "Enemy"):
        enemy.decreaseHealth(self._damage)