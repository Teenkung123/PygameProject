import random
import pygame
import logging
from typing import TYPE_CHECKING

from src.GameMechanics.Entities.Enemy import Enemy
from src.Events import PLAYER_VICTORY

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
        self.__waiting = False        # Waiting for next wave
        self.__delay = 0.0            # Time since wave completed

        self.__victory = False        # Is Victory

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
        self.__checkWaiting(deltaTime)
        self.__spawnRandomEnemy(deltaTime)
        self.__checkWaveCompleted()
        self.__updateEnemies(deltaTime)

    def draw(self, screen):
        try:
            self.__spawnedEnemy.draw(screen)
        except Exception as e:
            logging.error(f"Error drawing enemies: {e}")

    def getEnemies(self) -> pygame.sprite.Group:
        return self.__spawnedEnemy

    def __checkWaiting(self, deltaTime: float):
        if self.__victory:
            return
        if self.__waiting:
            self.__delay += deltaTime
            wave_delay = self.__main.getConfig().getGameSettings("wave_delay")
            if wave_delay is None:
                wave_delay = 3.0  # Default to 3 seconds if not set
            if self.__delay >= wave_delay:
                self.__waiting = False
                self.__delay = 0.0
                self.startNextWave()
            return

        if self.__currentWave == 0:
            self.startNextWave()

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
        self.__waiting = True
        self.__spawnTimer = 0.0

    def __updateEnemies(self, deltaTime: float):
        try:
            self.__spawnedEnemy.update(deltaTime)
        except Exception as e:
            logging.error(f"Error updating WaveManager: {e}")


