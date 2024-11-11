import pygame

from src import Events
from typing import TYPE_CHECKING

from src.MainMenuMechanics.MainMenuEventHandler import MainMenuEventHandler
from src.Scenes.GameScene import GameScene

if TYPE_CHECKING:
    from Game import Main

class EventHandler:
    def __init__(self, main: 'Main'):
        self.__main = main
        self.__mainMenuHandler = MainMenuEventHandler(main)

    def handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__main.setRunning(False)

            if self.__main.getCurrentSceneName() == "main":
                self.__mainMenuHandler.handle(event)

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        x = x // 64
                        y = y // 64
                        scene.getPlacementManager().place("dispenser", (x, y))
                #TODO: VICTORY EVENT
