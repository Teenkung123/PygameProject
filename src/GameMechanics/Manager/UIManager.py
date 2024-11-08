from typing import TYPE_CHECKING

import pygame.font

from src.GameMechanics.Elements.UI.EnemyHealthBar import EnemyHealthBar
from src.GameMechanics.Elements.UI.GameOverUI import GameOverUI
from src.GameMechanics.Elements.UI.HealthBarUI import HealthBarUI

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class UIManager:
    def __init__(self, gameScene: 'GameScene'):
        self.__gameOverUI = GameOverUI(gameScene)
        self.__healthUI = HealthBarUI(gameScene)
        self.__EnemyHealthUI = EnemyHealthBar(gameScene)

    def displayGameOver(self):
        self.__gameOverUI.display()

    def updateHealthBar(self):
        self.__healthUI.display()

    def updateEnemyHealthBar(self):
        self.__EnemyHealthUI.display()

