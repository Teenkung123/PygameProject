from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    import Main

class MainMenuEventHandler:
    def __init__(self, main: 'Main'):
        self.__main = main

    def handle(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.__main.setCurrentScene("game")