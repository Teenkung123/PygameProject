
import pygame
import sys
import os
import json
import logging
from ConfigLoader import ConfigLoader
from src import Events
from src.Elements.Screen import Screen
from src.Entities.Player import Player
from src.Manager.EnemyManager import EnemyManager
from src.Manager.StageManager import StageManager
from src.Manager.UIManager import UIManager
from src.Manager.WaveManager import WaveManager

ENEMY_REACHED_END = pygame.USEREVENT + 1

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("game.log"),
        logging.StreamHandler()
    ]
)

class Main:
    def __init__(self):
        # Determine the project root directory
        self.__projectRoot = os.path.dirname(os.path.abspath(__file__))
        logging.info(f"Project Root: {self.__projectRoot}")
        pygame.init()
        self.__config = ConfigLoader(os.path.join(self.__projectRoot, "config", "config.json"))
        self.__enemyManager = EnemyManager(self)
        self.__screen = Screen(self).getScreen()
        self.__stageManager = StageManager(self, "default")
        self.__UIManager = UIManager(self)
        self.__player = Player(self)
        self.__enemyConfig = self.__enemyManager.getEnemiesConfig()
        self.__path = self.__stageManager.getPath().get_path()

        # Initialize WaveManager
        try:
            game_settings = self.__config.getConfig().get("game_settings", {})
            self.__waveManager = WaveManager(
                self.__stageManager.getStageConfig().getConfig().get("waves", {}),
                self.__enemyConfig,
                self.__path,
                self.__stageManager.getStageConfig().getGridSize(),
                self.__projectRoot,
                game_settings
            )
        except Exception as e:
            logging.error(f"Failed to initialize WaveManager: {e}")
            sys.exit(1)

        # Retrieve player health for display purposes
        self.player_health = self.__waveManager.player_health

        # Set up fonts
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == Events.GAME_OVER:
                    running = False
                elif event.type == Events.ENEMY_REACHED_END:
                    self.__player.doDamage(event.enemy)

            # Update wave manager and enemies
            try:
                self.__waveManager.update(dt)
            except Exception as e:
                logging.error(f"Error updating WaveManager: {e}")

            # Draw the path and background
            try:
                self.__stageManager.getBackground().draw()
                self.__stageManager.getPath().draw()
            except Exception as e:
                logging.error(f"Error drawing StageManager: {e}")

            # Draw enemies
            try:
                self.__waveManager.draw(self.__screen)
            except Exception as e:
                logging.error(f"Error drawing enemies: {e}")

            self.__UIManager.updateHealthBar()

            # Update the display
            try:
                pygame.display.flip()
            except Exception as e:
                logging.error(f"Error updating display: {e}")

        # Display Game Over Screen
        self.__UIManager.displayGameOver()
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    def getConfig(self) -> ConfigLoader:
        return self.__config

    def getScreen(self) -> pygame.Surface:
        return self.__screen

    def getProjectRoot(self) -> str:
        return self.__projectRoot

    def getStageManager(self) -> StageManager:
        return self.__stageManager

    def getWaveManager(self) -> WaveManager:
        return self.__waveManager

    def getEnemyManager(self) -> EnemyManager:
        return self.__enemyManager

    def getPlayer(self) -> Player:
        return self.__player

if __name__ == "__main__":
    Main().run()
