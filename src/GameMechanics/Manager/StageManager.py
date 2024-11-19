import logging

import pygame

from src.Utils import Events
from src.GameMechanics.Elements.BackgroundElement import BackgroundElement
from src.GameMechanics.Elements.PathElement import PathElement
from src.GameMechanics.Configs.StageConfig import StageConfig
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
        self.timeScale = 1.0 #Time Scale, Use in events like time slow or speed up some element of the game, like time stop skill
        self.__isPaused = False
        self.isVictory = False
        self.isLost = False


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

    def tick(self, deltaTime: float):
        if self.__main.getUIManager().pauseUI.getPauseTimeMultiplier() > 0 and not self.isVictory and not self.isLost:
            self.__main.getWaveManager().update(deltaTime)
            self.__main.getPlacementManager().tick(deltaTime)
            self.__main.getUIManager().currencyUI.tick(deltaTime)
            self.__main.getUIManager().debuffIndicator.tick(deltaTime)

        self.__main.getStageManager().getBackground().draw()
        self.__main.getStageManager().getPath().draw()
        self.__main.getPlacementManager().draw()
        self.__main.getWaveManager().draw()

        self.__main.getUIManager().getHurtUI().tick(deltaTime)
        self.__main.getUIManager().updateHealthBar()
        self.__main.getUIManager().updateCurrency()
        self.__main.getUIManager().updateEnemyHealthBar()
        self.__main.getUIManager().updateHotbarInventory()

        self.__main.getUIManager().debuffIndicator.draw()

        if self.__main.getUIManager().pauseUI.getPauseTimeMultiplier() > 0:
            self.__main.getUIManager().towerStatusUI.draw()
            self.__main.getUIManager().waveChangeUI.tick(deltaTime)

        if self.isVictory:
            self.__main.getUIManager().playerVictoryUI.tick(deltaTime)

        if self.isLost:
            self.__main.getUIManager().playerLostUI.tick(deltaTime)

        self.__main.getUIManager().pauseUI.tick(deltaTime)
    # noinspection PyMethodMayBeStatic
    def gameOver(self):
        pygame.event.post(pygame.event.Event(Events.PLAYER_GAME_OVER))

    def pauseGame(self, state: bool = None):
        if state is not None:
            logging.info(f"Game Paused: {state}")
            self.__isPaused = state
        else:
            self.__isPaused = not self.__isPaused

    def isPaused(self):
        return self.__isPaused
