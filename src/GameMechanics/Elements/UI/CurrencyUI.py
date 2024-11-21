import math
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene


class CurrencyUI:
    def __init__(self, gameScene: 'GameScene'):
        self.__main = gameScene
        self.__font = gameScene.getFont(12)
        self.__heartImg = pygame.image.load("config/images/UI/gold_ingot.png")
        self.__heartImg = pygame.transform.scale(self.__heartImg, (30, 30))
        self.__tick = 0
        self.__maxTick = 0.25

    def __drawBar(self):
        player = self.__main.getPlayer()

        bar_x = 30
        bar_y = 40
        bar_width = self.__main.getStageManager().getStageConfig().getGridSize()*2
        bar_height = self.__main.getStageManager().getStageConfig().getGridSize()*0.33
        self.__background = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        red_color = max((self.__tick/self.__maxTick) * 255, 1)
        pygame.draw.rect(self.__main.getScreen(), (red_color, 0, 0), self.__background)
        self.__main.getScreen().blit(self.__heartImg, (bar_x - 14, bar_y-6))



    def __drawText(self):
        screen = self.__main.getScreen()

        text = self.__font.render(f"{self.__main.getCurrencyManager().getCurrency('gold')}", True, (255, 200, 0))
        text_rect = text.get_rect()

        bar_center = self.__background.center

        text_rect.center = bar_center

        screen.blit(text, text_rect)

    def display(self):
        self.__drawBar()
        self.__drawText()

    def tick(self, dt: float):
        if self.__tick > 0:
            self.__tick -= dt
        pass

    def setTick(self):
        self.__tick = self.__maxTick
        pass

