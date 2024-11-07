from typing import TYPE_CHECKING

import pygame

from ConfigLoader import ConfigLoader
from src.GameMechanics.Entities.Player import Player
from src.GameMechanics.EnemyConfig import EnemyConfig
from src.GameMechanics.Manager.StageManager import StageManager
from src.GameMechanics.Manager.UIManager import UIManager
from src.GameMechanics.Manager.WaveManager import WaveManager
from src.Scenes.Scene import Scene

if TYPE_CHECKING:
    import Main

class GameScene(Scene):
    def __init__(self, main: 'Main'):
        super().__init__()
        self.__main = main
        self.__enemyConfig = EnemyConfig(self)
        self.__stageManager = StageManager(self, "default")
        self.__UIManager = UIManager(self)
        self.__player = Player(self)
        self.__waveManager = WaveManager(self)

    def tick(self, dt: float):
        self.__stageManager.tick(dt)

    def reset(self):
        self.__enemyConfig = EnemyConfig(self)
        self.__stageManager = StageManager(self, "default")
        self.__UIManager = UIManager(self)
        self.__player = Player(self)
        self.__waveManager = WaveManager(self)

    def getConfig(self) -> ConfigLoader:
        return self.__main.getConfig()

    def getProjectRoot(self) -> str:
        return self.__main.getProjectRoot()

    def getScreen(self) -> pygame.Surface:
        return self.__main.getScreen()

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
