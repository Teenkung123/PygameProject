import random
import pygame
import logging
from typing import TYPE_CHECKING

from src.GameMechanics.Entities.Enemy import Enemy
from src.Utils.Events import PLAYER_VICTORY, STAGE_WAVE_END

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class WaveManager:
    def __init__(self, gameScene: 'GameScene'):
        self.__main = gameScene
        self.__waveConfig = gameScene.getStageManager().getStageConfig().getConfig().get("waves", {})
        self.__enemyConfig = gameScene.getEnemyConfig().getConfig()

        self.__spawnTimer = 0.0       # Time since last enemy spawn
        self.__spawnRate = 2.0        # Time between enemy spawns (default)
        self.__enemies = []           # List of enemies to spawn

        self.__currentWave = 0        # Current wave number
        self.__delay = 0.0            # Time since wave completed

        self.__spawnedEnemy = pygame.sprite.Group()  # Group of spawned enemies

        logging.info("WaveManager initialized.")

    def startNextWave(self):
        self.__currentWave += 1
        wave_key = str(self.__currentWave)
        if wave_key in self.__waveConfig:
            wave_info = self.__waveConfig[wave_key]
            self.__spawnRate = wave_info.get("spawn_rate", 2.0)
            if not isinstance(self.__spawnRate, (int, float)) or self.__spawnRate <= 0:
                logging.warning(f"Invalid spawn_rate '{self.__spawnRate}' in wave {self.__currentWave}. Using default 2.0.")
                self.__spawnRate = 2.0

            enemies = wave_info.get("enemies", {})
            if not enemies:
                logging.warning(f"No enemies defined for wave {self.__currentWave}.")
            for enemy_type, count in enemies.items():
                if enemy_type not in self.__enemyConfig:
                    logging.error(f"Enemy type '{enemy_type}' not defined in enemies configuration.")
                    continue
                if not isinstance(count, int) or count <= 0:
                    logging.warning(f"Invalid count '{count}' for enemy '{enemy_type}' in wave {self.__currentWave}. Skipping.")
                    continue
                for _ in range(count):
                    self.__enemies.append(enemy_type)
            logging.info(f"Wave {self.__currentWave} started with {len(self.__enemies)} enemies.")
        else:
            logging.info("All waves completed. Victory!")
            pygame.event.post(pygame.event.Event(PLAYER_VICTORY))

    def update(self, deltaTime: float):
        if self.__main.getUIManager().waveChangeUI.canStart:
            self.__spawnRandomEnemy(deltaTime)
            self.__checkWaveCompleted()
            self.__updateEnemies(deltaTime)

    def draw(self):
        try:
            self.__spawnedEnemy.draw(self.__main.getScreen())
        except Exception as e:
            logging.error(f"Error drawing enemies: {e}")

    def getEnemies(self) -> pygame.sprite.Group:
        return self.__spawnedEnemy

    def __spawnRandomEnemy(self, deltaTime: float):
        if self.__enemies:
            self.__spawnTimer += deltaTime
            if self.__spawnTimer >= self.__spawnRate:
                enemy_type = self.__selectRandomEnemy()
                self.__spawnEnemy(enemy_type)
                self.__spawnTimer = 0.0

    def __selectRandomEnemy(self):
        selected = random.choice(self.__enemies)
        self.__enemies.remove(selected)
        return selected

    def __spawnEnemy(self, enemyType: str):
        try:
            enemy = Enemy(self.__main, enemyType)
            enemy.spawn()
            # noinspection PyTypeChecker
            self.__spawnedEnemy.add(enemy)
            logging.info(f"Spawned enemy: {enemyType.capitalize()}")
        except FileNotFoundError as e:
            logging.error(e)
        except Exception as e:
            logging.error(f"Unexpected error spawning enemy '{enemyType}': {e}")

    def __checkWaveCompleted(self):
        if not self.__enemies and not self.__spawnedEnemy:
            self.completeWave()

    def completeWave(self):
        if str(self.__currentWave + 1) in self.__waveConfig:
            self.__spawnTimer = 0.0
            pygame.event.post(pygame.event.Event(STAGE_WAVE_END, wave=self.__currentWave))
        else:
            logging.info("All waves completed. Victory!")
            pygame.event.post(pygame.event.Event(PLAYER_VICTORY))

    def __updateEnemies(self, deltaTime: float):
        try:
            self.__spawnedEnemy.update(deltaTime)
        except Exception as e:
            logging.error(f"Error updating WaveManager: {e}")