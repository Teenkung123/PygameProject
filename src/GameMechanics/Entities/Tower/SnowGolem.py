import logging
import pygame

from src.GameMechanics.Entities.Tower.Tower import Tower
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Entities.Enemy import Enemy

class SnowGolem(Tower):
    def _getConfigFileName(self):
        return "snow_golem.json"

    def _applyEffect(self, enemy: "Enemy"):
        enemy.setSpeedMultiplier("snow_golem", 0.25, 5000)
        enemy.decreaseHealth(self._damage)
