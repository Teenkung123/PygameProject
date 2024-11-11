from typing import TYPE_CHECKING

import pygame


if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene


class HotbarEvent:
    def __init__(self, gameScene: 'GameScene'):
        self.__gameScene = gameScene


    def handleEvent(self, event: pygame.event.Event):
        pass
