from typing import TYPE_CHECKING

import pygame.font

from src.Elements.UI.GameOverUI import GameOverUI
from src.Elements.UI.HealthBarUI import HealthBarUI

if TYPE_CHECKING:
    from Main import Main

class UIManager:
    def __init__(self, main: 'Main'):
        self.__gameOverUI = GameOverUI(main)
        self.__healthUI = HealthBarUI(main, pygame.font.Font(None, 36))

    def displayGameOver(self):
        self.__gameOverUI.display()

    def updateHealthBar(self):
        self.__healthUI.display()

