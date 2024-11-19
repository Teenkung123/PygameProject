from typing import TYPE_CHECKING

import pygame

from src.Scenes.MainMenuScene import MainMenuScene

if TYPE_CHECKING:
    from pygame.event import Event
    import Main

class MainMenuEventHandler:
    def __init__(self, main: 'Main'):
        self.__main = main

    def handle(self, event: 'Event'):
        scene: MainMenuScene = self.__main.getCurrentScene()
        scene.startBtn.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.__main.setCurrentScene("game")
