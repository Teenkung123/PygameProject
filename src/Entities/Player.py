from typing import TYPE_CHECKING

import pygame

from src import Events
from src.Events import PLAYER_DAMAGED

if TYPE_CHECKING:
    from Game import Main
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
        self.decreaseHealth(enemy.getDamage())
        pygame.event.post(pygame.event.Event(PLAYER_DAMAGED, enemy=enemy))

    # noinspection PyMethodMayBeStatic
    def gameOver(self):
        pygame.event.post(pygame.event.Event(Events.PLAYER_GAME_OVER))

    def __checkGameOver(self):
        if self.__health <= 0:
            self.gameOver()