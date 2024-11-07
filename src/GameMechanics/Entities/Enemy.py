import logging
import os.path
from typing import TYPE_CHECKING

import pygame

from src import Events
from src.Events import ENEMY_REACHED_END

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class Enemy(pygame.sprite.Sprite):
    def __init__(self, gameScene: 'GameScene', enemyType: str):
        super().__init__()
        self.__position = None
        self.__main = gameScene
        self.__type = enemyType
        self.__config = gameScene.getEnemyConfig().getConfig()[enemyType]
        self.__walkPath = gameScene.getStageManager().getStageConfig().getWalkPath()
        self.__gridSize = gameScene.getStageManager().getStageConfig().getGridSize()
        self.__speedMultiplier = 1.0
        self.__sizeMultiplier = 0.8
        self.__currentNode = 0
        self.__health = 100
        self.__damage = 10
        self.__speed = 100
        self.image = None
        self.__loadEnemy()

    def __loadEnemy(self):
        if not self.__config:
            logging.error(f"No configuration found for enemy type '{self.__type}'.")
            raise ValueError(f"No configuration found for enemy type '{self.__type}'.")

        self.__speed = self.__config["speed"] if "speed" in self.__config else 100
        self.__damage = self.__config["damage"] if "damage" in self.__config else 10
        self.__health = self.__config["health"] if "health" in self.__config else 100
        self.image = None
        self.__loadImage()

    def __loadImage(self):
        self.__imagePath = os.path.join(self.__main.getProjectRoot(), self.__config["image"])
        self.__imagePath = os.path.normpath(self.__imagePath)
        if not os.path.exists(self.__imagePath):
            raise FileNotFoundError(f"Enemy image not found: {self.__imagePath}")
        try:
            self.image = pygame.image.load(self.__imagePath).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.__main.getStageManager().getStageConfig().getGridSize() * self.__sizeMultiplier, self.__main.getStageManager().getStageConfig().getGridSize() * self.__sizeMultiplier))
            logging.debug(logging.INFO, f"Loaded image for '{self.__type}' and scaled to ({self.__main.getStageManager().getStageConfig().getGridSize() * self.__sizeMultiplier}x{self.__main.getStageManager().getStageConfig().getGridSize() * self.__sizeMultiplier}).")
        except pygame.error as e:
            raise pygame.error(f"Error loading enemy image '{self.__imagePath}': {e}")

        self.rect = self.image.get_rect()

    def spawn(self):
        try:
            x, y = map(int, self.__walkPath[0].split(","))
            self.__position = pygame.math.Vector2(x * self.__gridSize + (self.__gridSize/2), y * self.__gridSize + (self.__gridSize/2))
            self.rect.center = self.__position
            logging.debug(f"Enemy spawned at {self.__position}.")
        except IndexError:
            logging.error("No path defined for enemy.")
            raise
        
    def update(self, deltaTime: float):
        if not self.alive():
            return
        if self.__currentNode >= len(self.__walkPath) - 1:
            self.kill()
            pygame.event.post(pygame.event.Event(ENEMY_REACHED_END, enemy=self))
            logging.info(f"Enemy reached the end.")
            return

        x, y = map(int, self.__walkPath[self.__currentNode + 1].split(","))
        target = pygame.math.Vector2(x * self.__gridSize + (self.__gridSize/2), y * self.__gridSize + (self.__gridSize/2))
        
        direction = target - self.__position
        distance = direction.length()
        
        if distance == 0:
            self.__currentNode += 1
            return
        direction = direction.normalize()
        
        movement = direction * self.__speed * deltaTime
        if movement.length() > distance:
            self.__position = target
            self.__currentNode += 1
        else:
            self.__position += movement
            
        self.rect.center = self.__position
        
    def draw(self):
        try:
            self.__main.getScreen().blit(self.image, self.rect)
        except Exception as e:
            logging.error(f"Error drawing enemy: {e}")

    def killEnemy(self):
        self.kill()
        pygame.event.post(Events.ENEMY_KILLED)

    def getPosition(self):
        return self.__position

    def getRect(self):
        return self.rect

    def getDamage(self):
        return self.__damage

    def getHealth(self):
        return self.__health

    def getSpeed(self):
        return self.__speed

    def setSpeed(self, speed: int):
        self.__speed = speed

    def getSpeedMultiplier(self):
        return self.__speedMultiplier

    def setSpeedMultiplier(self, multiplier: float):
        self.__speedMultiplier = multiplier

    def setHealth(self, health: int):
        self.__health = health
        if self.__health <= 0:
            self.kill()

    def decreaseHealth(self, damage: int):
        self.__health -= damage
        if self.__health <= 0:
            self.kill()

    def isAlive(self):
        return self.__health > 0 and self.alive()

    def getType(self):
        return self.__type
