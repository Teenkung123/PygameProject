from typing import TYPE_CHECKING

import pygame.event

from src.Utils.Events import PLAYER_EXIT
from src.Utils.Button import Button

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class PlayerVictoryUI:
    def __init__(self, scene: 'GameScene'):
        self.__scene = scene
        self.__width = scene.getScreen().get_width()
        self.__height = scene.getScreen().get_height()
        self.__background = Button(x=0, y=0, w=scene.getScreen().get_width(), h=scene.getScreen().get_height(), color=(0, 0, 0), alpha=0, visible=False)
        self.__title = self.__scene.getFont(64).render("", True, (255, 255, 255)).convert_alpha()
        self.__subtitle = self.__scene.getFont(32).render("", True, (255, 255, 255)).convert_alpha()
        self.__tick = 0
        self.__fadeIn = 3

    def set(self, tick):
        self.__tick = tick

    def tick(self, dt: float, ):
        if self.__scene.getStageManager().isVictory:
            self.__tick += dt
            self.__background.visible = True
            self.__setTitle()
            alpha255 = min(255, int(255 * min(self.__fadeIn, self.__tick) / self.__fadeIn))
            alpha200 = min(200, int(200 * min(self.__fadeIn, self.__tick) / self.__fadeIn))
            self.__background.alpha = alpha200
            self.__title.set_alpha(alpha255)
            self.__subtitle.set_alpha(alpha255)
            self.__background.draw(self.__scene.getScreen())
            self.__scene.getScreen().blit(self.__title, (self.__width // 2 - self.__title.get_width() // 2, self.__height // 2 - self.__title.get_height() // 2))
            self.__scene.getScreen().blit(self.__subtitle, (self.__width // 2 - self.__subtitle.get_width() // 2, self.__height // 2 + self.__title.get_height() // 2))
            if (10 - int(self.__tick)) <= 0:
                pygame.event.post(pygame.event.Event(PLAYER_EXIT))

    def __setTitle(self):
        if self.__tick < 5:
            self.__title = self.__scene.getFont(64).render("Victory", True, (0, 255, 0)).convert_alpha()
            self.__subtitle = self.__scene.getFont(32).render("You have completed the stage", True, (255, 255, 255)).convert_alpha()
        elif self.__tick >= 5:
            self.__title = self.__scene.getFont(64).render("Returning to Main Menu in", True, (0, 255, 0)).convert_alpha()
            self.__subtitle = self.__scene.getFont(32).render(f"{10 - int(self.__tick)}", True, (255, 255, 255)).convert_alpha()