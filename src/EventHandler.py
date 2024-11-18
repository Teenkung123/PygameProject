import pygame

from src import Events
from typing import TYPE_CHECKING
import logging
from src.Events import START_GAME
from src.GameMechanics.Events.GameSceneHandler import GameSceneHandler
from src.MainMenuMechanics.MainMenuEventHandler import MainMenuEventHandler
from src.Scenes.GameScene import GameScene

if TYPE_CHECKING:
    from Game import Main

class EventHandler:
    def __init__(self, main: 'Main'):
        self.__main = main
        self.__mainMenuHandler = MainMenuEventHandler(main)
        self.__gameSceneHandler = GameSceneHandler(main)

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__main.setRunning(False)
                
            if event.type == START_GAME:
                logging.info("triggered")

            if self.__main.getCurrentSceneName() == "main":
                self.__mainMenuHandler.handle(event)

            if self.__main.getCurrentSceneName() == "game":
                self.__gameSceneHandler.handle(event)
