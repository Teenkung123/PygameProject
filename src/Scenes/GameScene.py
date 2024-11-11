import pygame

from typing import TYPE_CHECKING
from ConfigLoader import ConfigLoader
from src.GameMechanics.Entities.Player import Player
from src.GameMechanics.Configs.EnemyConfig import EnemyConfig
from src.GameMechanics.Manager.InventoryManager import InventoryManager
from src.GameMechanics.Manager.PlacementManager import PlacementManager
from src.GameMechanics.Manager.StageManager import StageManager
from src.GameMechanics.Manager.UIManager import UIManager
from src.GameMechanics.Manager.WaveManager import WaveManager
from src.GradientUtils import GradientUtils
from src.Scenes.Scene import Scene

if TYPE_CHECKING:
    import Main

class GameScene(Scene):
    def __init__(self, main: 'Main'):
        super().__init__()
        self.__main: 'Main' = main
        self.__enemyConfig = EnemyConfig(self)
        self.__stageManager = StageManager(self, "default")
        self.__UIManager = UIManager(self)
        self.__player = Player(self)
        self.__waveManager = WaveManager(self)
        self.__placementManager = PlacementManager(self)
        self.__InventoryManager = InventoryManager(self, self.__UIManager.hotbarUI)

    def tick(self, dt: float):
        self.__stageManager.tick(dt)

    def reset(self):
        self.__enemyConfig = EnemyConfig(self)
        self.__stageManager = StageManager(self, "default")
        self.__UIManager = UIManager(self)
        self.__player = Player(self)
        self.__waveManager = WaveManager(self)
        self.__placementManager = PlacementManager(self)
        self.__InventoryManager = InventoryManager(self, self.__UIManager.hotbarUI)

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

    def getGradientUtils(self) -> GradientUtils:
        return self.__main.getGradientUtils()

    def getFont(self, size: int) -> pygame.font.Font:
        return self.__main.getFont(size)

    def getPlacementManager(self) -> PlacementManager:
        return self.__placementManager

    def getInventoryManager(self) -> InventoryManager:
        return self.__InventoryManager