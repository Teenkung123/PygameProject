import logging
from typing import TYPE_CHECKING

import pygame

from src.GameMechanics.Entities.Tower.Tower import Tower

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class Dispenser(Tower):
    def __init__(self, gameScene: "GameScene"):
        super().__init__()
        self.__gameScene = gameScene
        self.__gridSize = self.__gameScene.getStageManager().getStageConfig().getGridSize()
        self.__position = None
        self.__truePosition = None
        self.__isPlaced = False
        self.__cooldown = 2.0
        self.__reach = 3
        self.__damage = 40

    def tick(self, dt: float):
        if self.__isPlaced:
            self.__cooldown -= dt
            if self.__cooldown <= 0:
                self.attack()
            self.draw()

    def draw(self):
        rect = pygame.Rect(self.__position[0] * self.__gridSize, self.__position[1] * self.__gridSize, self.__gridSize, self.__gridSize)
        pygame.draw.rect(self.__gameScene.getScreen(), (255, 0, 0, 64), rect)

    def place(self, position: tuple[int, int]):
        self.__position = position
        self.__truePosition = pygame.math.Vector2(position[0] * self.__gridSize, position[1] * self.__gridSize)
        self.__isPlaced = True

    def attack(self):
        for enemy in self.__gameScene.getWaveManager().getEnemies():
            enemyLoc = pygame.math.Vector2(enemy.rect.centerx, enemy.rect.centery)
            if enemyLoc.distance_to(self.__truePosition) < self.__reach * self.__gridSize:
                enemy.decreaseHealth(self.__damage)
                self.__cooldown = 2.0
                break
        self.__cooldown = 2.0
