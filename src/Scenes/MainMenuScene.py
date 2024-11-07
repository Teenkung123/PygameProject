import logging

import pygame

from src.Scenes.Scene import Scene
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import Main

class MainMenuScene(Scene):
    def __init__(self, main: 'Main'):
        super().__init__()
        self.__main = main
        self.__screen = main.getScreen()

    def tick(self, dt: float):
        self.__screen.fill((30, 30, 30))
        font = pygame.font.Font(None, 74)
        text = font.render("Main Menu - Press Enter to Start", True, (255, 255, 255))
        self.__screen.blit(text, (50, 50))

    def reset(self):
        pass