import math
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene


class HealthBarUI:
    def __init__(self, gameScene: 'GameScene'):
        self.__main = gameScene
        self.__font = gameScene.getFont(12)
        self.__heartImg = pygame.image.load("config/images/heart.png")
        self.__heartImg = pygame.transform.scale(self.__heartImg, (30, 30))

    def __drawBar(self):
        player = self.__main.getPlayer()

        bar_x = 30
        bar_y = 10
        bar_width = self.__main.getStageManager().getStageConfig().getGridSize()*2
        bar_height = self.__main.getStageManager().getStageConfig().getGridSize()*0.33

        self.__maxHealth = pygame.Rect(bar_x, bar_y, bar_width, bar_height)

        health_ratio = player.getHealth() / player.getMaxHealth()
        current_health_width = max(int(bar_width * health_ratio), 1)
        currentHealth = self.__main.getGradientUtils().get_horizontal_gradient(current_health_width, bar_height, [(255, 0, 0), (255, 128, 0)])

        pygame.draw.rect(self.__main.getScreen(), (136, 28, 16), self.__maxHealth)
        self.__main.getScreen().blit(currentHealth, (bar_x, bar_y))
        pygame.draw.rect(self.__main.getScreen(), (0, 0, 0), self.__maxHealth, 2)
        self.__main.getScreen().blit(self.__heartImg, (bar_x - 14, bar_y-2))

    def __drawText(self):
        player = self.__main.getPlayer()
        screen = self.__main.getScreen()

        health_text = self.__font.render(f"{player.getHealth()}/{player.getMaxHealth()}", True, (255, 255, 255))
        text_rect = health_text.get_rect()

        bar_center = self.__maxHealth.center

        text_rect.center = bar_center

        screen.blit(health_text, text_rect)

    def display(self):
        self.__drawBar()
        self.__drawText()
