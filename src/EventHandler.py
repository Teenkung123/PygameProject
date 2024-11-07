import pygame

from src import Events


class EventHandler:
    def __init__(self, main):
        self.__main = main

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == Events.PLAYER_GAME_OVER:
                self.__main.setRunning(False)
            elif event.type == Events.ENEMY_REACHED_END:
                self.__main.getPlayer().doDamage(event.enemy)
            #TODO: VICTORY EVENT