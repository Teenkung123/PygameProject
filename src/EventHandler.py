import pygame

from src import Events
from typing import TYPE_CHECKING

from src.Scenes.GameScene import GameScene

if TYPE_CHECKING:
    from Game import Main

class EventHandler:
    def __init__(self, main: 'Main'):
        self.__main = main

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__main.setRunning(False)

            if self.__main.getCurrentSceneName() == "main":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.__main.setCurrentScene("game")

            if self.__main.getCurrentSceneName() == "game":
                scene: GameScene = self.__main.getCurrentScene()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.__main.setCurrentScene("main")
                    self.__main.resetScene("game")
                if event.type == Events.PLAYER_GAME_OVER:
                    scene.getUIManager().displayGameOver()
                    self.__main.setRunning(False)
                elif event.type == Events.ENEMY_REACHED_END:
                    scene.getPlayer().doDamage(event.enemy)
                #TODO: VICTORY EVENT