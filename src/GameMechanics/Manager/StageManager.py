import logging

import pygame

from src import Events
from src.GameMechanics.Elements.BackgroundElement import BackgroundElement
from src.GameMechanics.Elements.PathElement import PathElement
from src.GameMechanics.Entities.Tower.Dispenser import Dispenser
from src.GameMechanics.StageConfig import StageConfig
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class StageManager:
    
    def __init__(self, gameScene: 'GameScene', stage: str):
        self.__main = gameScene
        logging.info(f"StageManager Initialized with Project Root: {gameScene.getProjectRoot()}")

        self.__stageConfig = StageConfig(gameScene.getProjectRoot(), stage)
        self.__background = BackgroundElement(self.__stageConfig, gameScene.getConfig(), gameScene.getScreen())
        self.__path = PathElement(self.__stageConfig, gameScene, gameScene.getScreen())
        self.__timeScale = 1.0 #Time Scale, Use in events like time slow or speed up some element of the game, like time stop skill


    def getStageConfig(self):
        """
        Return the StageConfig instance.
        """
        return self.__stageConfig
    
    def getBackground(self):
        """
        Return the BackgroundElement instance.
        """
        return self.__background
    
    def getPath(self):
        """
        Return the PathElement instance.
        """
        return self.__path

    def getTimeScale(self):
        """
        Return the timescale.
        """
        return self.__timeScale

    def tick(self, deltaTime: float):
        try:
            self.__main.getWaveManager().update(deltaTime)
        except Exception as e:
            logging.error(f"Error updating WaveManager: {e}")

        # Draw the path and background
        try:
            self.__main.getStageManager().getBackground().draw()
            self.__main.getStageManager().getPath().draw()
        except Exception as e:
            logging.error(f"Error drawing StageManager: {e}")

        # Draw towers
        self.__main.getPlacementManager().tick(deltaTime)

        # Draw enemies
        try:
            self.__main.getWaveManager().draw(self.__main.getScreen())
        except Exception as e:
            logging.error(f"Error drawing enemies: {e}")


        self.__main.getUIManager()
        self.__main.getUIManager().updateHealthBar()
        self.__main.getUIManager().updateEnemyHealthBar()

    # noinspection PyMethodMayBeStatic
    def gameOver(self):
        pygame.event.post(pygame.event.Event(Events.PLAYER_GAME_OVER))