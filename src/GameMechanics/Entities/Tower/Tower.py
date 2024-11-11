import os
import json
import logging
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Entities.Enemy import Enemy

class Tower(pygame.sprite.Sprite):
    def __init__(self, gameScene: "GameScene"):
        super().__init__()
        self._gameScene = gameScene
        self._rect = None
        self._gridSize = self._gameScene.getStageManager().getStageConfig().getGridSize()
        self._position = None
        self._truePosition = None
        self._isPlaced = False
        self._config = None
        self._level = 1
        self._damage = 0
        self._cooldown = 0
        self._speed = 0
        self._range = 0
        self._cost = 0
        self._image = None
        self._loadTowerFile()
        self._loadImage()

    def _getConfigFileName(self):
        """Return the filename of the configuration file. Should be overridden by subclasses."""
        raise NotImplementedError

    def _loadTowerFile(self):
        filename = self._getConfigFileName()
        path = os.path.normpath(os.path.join(
            self._gameScene.getProjectRoot(),
            "config",
            "towers",
            filename
        ))

        if not os.path.exists(path):
            logging.error(f"{self.__class__.__name__} configuration file not found: {path}")
            raise FileNotFoundError(f"{self.__class__.__name__} configuration file not found: {path}")

        try:
            with open(path, "r") as f:
                towerConfig = json.load(f)
                self._config = towerConfig
                self._damage = towerConfig[f"{self._level}"]["damage"]
                self._speed = towerConfig[f"{self._level}"]["speed"]
                self._range = towerConfig[f"{self._level}"]["range"]
                self._cost = towerConfig[f"{self._level}"]["cost"]
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing {self.__class__.__name__} configuration: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error loading {self.__class__.__name__} configuration: {e}")
            raise

    def tick(self, dt: float):
        if self._isPlaced:
            self._cooldown -= dt
            if self._cooldown <= 0:
                self.attack()
            self.draw()

    def upgrade(self):
        if self._level < self._config["max_level"]:
            self._level += 1
            self._damage = self._config[f"{self._level}"]["damage"]
            self._speed = self._config[f"{self._level}"]["speed"]
            self._range = self._config[f"{self._level}"]["range"]
            self._cost = self._config[f"{self._level}"]["cost"]
            return True
        return False

    def draw(self):
        screen = self._gameScene.getScreen()
        if self._isPlaced and self._image:
            center = (
                self._truePosition.x + (self._gridSize - self._image.get_width()) // 2 - 32,
                self._truePosition.y + (self._gridSize - self._image.get_height()) // 2 - 32
            )
            screen.blit(self._image, center)

    def place(self, position: tuple[int, int]):
        self._position = position
        self._truePosition = pygame.math.Vector2(
            position[0] * self._gridSize + 32,
            position[1] * self._gridSize + 32
        )
        self._isPlaced = True
        self._rect = self._image.get_rect(center=self._truePosition)

    def attack(self):
        for enemy in self._gameScene.getWaveManager().getEnemies():
            enemy: "Enemy" = enemy
            enemyLoc = pygame.math.Vector2(enemy.rect.centerx, enemy.rect.centery)
            if enemyLoc.distance_to(self._truePosition) < self._range * self._gridSize:
                self._applyEffect(enemy)
                break
        self._cooldown = self._speed

    def _applyEffect(self, enemy: "Enemy"):
        """Apply the effect of this tower to the enemy. To be implemented by subclasses."""
        raise NotImplementedError

    def _loadImage(self):
        self._imagePath = os.path.join(
            self._gameScene.getProjectRoot(),
            self._config["image"]
        )
        self._imagePath = os.path.normpath(self._imagePath)
        if not os.path.exists(self._imagePath):
            raise FileNotFoundError(f"{self.__class__.__name__} image not found: {self._imagePath}")
        try:
            self._image = pygame.image.load(self._imagePath).convert_alpha()
            self._image = pygame.transform.scale(
                self._image,
                (int(self._gridSize * 0.8), int(self._gridSize * 0.8))
            )
            logging.debug(
                f"Loaded image for '{self.__class__.__name__}' and scaled to ({self._gridSize}x{self._gridSize})."
            )
        except pygame.error as e:
            raise pygame.error(f"Error loading {self.__class__.__name__} image '{self._imagePath}': {e}")
