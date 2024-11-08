import pygame
import sys
from src import Events


class EventHandler:
    def __init__(self, main):
        self.__main = main

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == Events.PLAYER_GAME_OVER:
                self.__main.running = False
            elif event.type == Events.ENEMY_REACHED_END:
                self.__main.getPlayer().doDamage(event.enemy)
            #TODO: VICTORY EVENT