import pygame

from typing import TYPE_CHECKING

from src.Utils import Events
from src.Utils.Events import PLAYER_INVENTORY_SELECTED, ENEMY_KILLED, PLAYER_EXIT, STAGE_WAVE_END, PLAYER_VICTORY
from src.GameMechanics.Events import EnemyKill
from src.GameMechanics.Events.EnemyReachEnd import EnemyReachEnd

if TYPE_CHECKING:
    from Game import Main
    from src.Scenes.GameScene import GameScene


class GameSceneHandler:
    def __init__(self, main: 'Main'):
        self.__main = main

    def handle(self, event):
        scene: GameScene = self.__main.getCurrentScene()
        scene.getUIManager().hotbarUI.handle_event(event)
        scene.getUIManager().pauseUI.handle_event(event)
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE) or (event.type == PLAYER_EXIT):
            self.__main.setCurrentScene("main")
            self.__main.resetScene("game")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            scene.getStageManager().pauseGame()
        if event.type == Events.PLAYER_GAME_OVER:
            scene.getStageManager().isLost = True
        elif event.type == Events.ENEMY_REACHED_END:
            EnemyReachEnd.handle(event, scene)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not scene.getStageManager().isPaused():
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    x = x // 64
                    y = y // 64
                    scene.getPlacementManager().place((x, y))

        elif event.type == PLAYER_INVENTORY_SELECTED:
            if not scene.getStageManager().isPaused():
                data = event.data
                scene.getInventoryManager().setSelectedTower(data.get("tower"))
        elif event.type == ENEMY_KILLED:

            EnemyKill.handle(event, scene, self.__main)
        elif event.type == STAGE_WAVE_END:
            if not scene.getStageManager().isVictory:
                if event.wave == 0:
                    scene.getWaveManager().startNextWave()
                    return
                scene.getUIManager().waveChangeUI.trigger(event.wave)
        elif event.type == PLAYER_VICTORY:
            scene.getStageManager().isVictory = True