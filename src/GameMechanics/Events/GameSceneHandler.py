import logging

import pygame

from typing import TYPE_CHECKING

from src import Events
from src.Events import PLAYER_INVENTORY_SELECTED

if TYPE_CHECKING:
    from Game import Main
    from src.Scenes.GameScene import GameScene


class GameSceneHandler:
    def __init__(self, main: 'Main'):
        self.__main = main

    def handle(self, event):
        scene: GameScene = self.__main.getCurrentScene()
        scene.getUIManager().hotbarUI.handle_event(event)
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
                scene.getPlacementManager().place((x, y))
        elif event.type == PLAYER_INVENTORY_SELECTED:
            data = event.data
            scene.getInventoryManager().setSelectedTower(data.get("tower"))
            logging.info(f"Inventory selected: {data}")
