from typing import TYPE_CHECKING

import pygame

from src import Events
from src.Events import PLAYER_DAMAGED

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Entities.Enemy import Enemy

class Player:
    def __init__(self, gameScene: 'GameScene'):
        self.__main = gameScene
        self.__maxHealth = gameScene.getConfig().getGameSettings("player_health")
        self.__health = self.__maxHealth

    def getHealth(self):
        return self.__health

    def getMaxHealth(self):
        return self.__maxHealth

    def setMaxHealth(self, maxHealth):
        self.__maxHealth = maxHealth

    def setHealth(self, health):
        if health > self.__maxHealth:
            health = self.__maxHealth
        self.__health = health
        self.__checkGameOver()

    def decreaseHealth(self, damage: int):
        self.__health -= damage
        self.__checkHealthOverflow()
        self.__checkGameOver()

    def doDamage(self, enemy: 'Enemy'):
        self.decreaseHealth(enemy.getDamage())
        pygame.event.post(pygame.event.Event(PLAYER_DAMAGED, enemy=enemy))

    def __checkGameOver(self):
        if self.__health <= 0:
            self.__main.getStageManager().gameOver()

    def __checkHealthOverflow(self):
        if self.__health > self.__maxHealth:
            self.__health = self.__maxHealth
        if self.__health < 0:
            self.__health = 0