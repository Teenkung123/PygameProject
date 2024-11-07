
import pygame
import sys
import os

from ConfigLoader import ConfigLoader
from src.Elements.Screen import Screen
from src.Entities.Player import Player
from src.EventHandler import EventHandler
from src.Manager.EnemyConfig import EnemyConfig
from src.Manager.StageManager import StageManager
from src.Manager.UIManager import UIManager
from src.Manager.WaveManager import WaveManager

class Main:
    def __init__(self):
        self.__running = True
        pygame.init()
        self.__projectRoot = os.path.dirname(os.path.abspath(__file__))
        self.__config = ConfigLoader(os.path.join(self.__projectRoot, "config", "config.json"))
        self.__enemyConfig = EnemyConfig(self)
        self.__screen = Screen(self)
        self.__stageManager = StageManager(self, "default")
        self.__UIManager = UIManager(self)
        self.__player = Player(self)
        self.__eventHandler = EventHandler(self)
        self.__waveManager = WaveManager(self)

    def run(self):
        clock = pygame.time.Clock()
        while self.__running:
            self.__eventHandler.handle()
            self.__screen.draw(clock.tick(60) / 1000.0)

        self.__UIManager.displayGameOver()
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    def getConfig(self) -> ConfigLoader:
        return self.__config

    def getScreen(self) -> pygame.Surface:
        return self.__screen.getScreen()

    def getProjectRoot(self) -> str:
        return self.__projectRoot

    def getStageManager(self) -> StageManager:
        return self.__stageManager

    def getWaveManager(self) -> WaveManager:
        return self.__waveManager

    def getEnemyConfig(self) -> EnemyConfig:
        return self.__enemyConfig

    def getPlayer(self) -> Player:
        return self.__player

    def getUIManager(self) -> UIManager:
        return self.__UIManager

    def setRunning(self, running: bool):
        self.__running = running