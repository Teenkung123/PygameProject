from typing import TYPE_CHECKING
import src.Events as e
import pygame
from pygame.locals import *

if TYPE_CHECKING:
    import Main

class MainMenuEventHandler:
    def __init__(self, main: 'Main'):
        self.__main = main

    def handle(self, event):
        if event.type == e.START_GAME:
            self.__main.setCurrentScene("game")