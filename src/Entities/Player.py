from typing import TYPE_CHECKING

import pygame

from src import Events

if TYPE_CHECKING:
    from Main import Main
    from src.Entities.Enemy import Enemy

class Player:
    def __init__(self, main: 'Main'):
        self.__main = main
        self.__health = main.getConfig().getGameSettings("player_health")

    def getHealth(self):
        return self.__health

    def setHealth(self, health):
        self.__health = health
        self.__checkGameOver()

    def decreaseHealth(self, damage: int):
        self.__health -= damage
        self.__checkGameOver()

    def doDamage(self, enemy: 'Enemy'):
        self.decreaseHealth(enemy.damage)

    def gameOver(self):
        pygame.event.post(Events.GAME_OVER)

    def __checkGameOver(self):
        if self.__health <= 0:
            self.gameOver()