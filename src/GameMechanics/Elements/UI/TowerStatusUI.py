from typing import TYPE_CHECKING

import pygame

from src.GameMechanics.Elements.Button import Button

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene


class TowerStatusUI:
    def __init__(self, scene: 'GameScene'):
        self.__scene = scene
        self.__width = scene.getScreen().get_width()
        self.__height = scene.getScreen().get_height()
        self.background = Button(
            0, 0, 200, 100,  # Initial width and height
            color=(0, 0, 0),
            alpha=0,
            border_color=(255, 255, 255, 0),
            border_width=2
        )
        self.__text_surfaces = []  # List to hold rendered text lines
        self.__tower_info = []     # List to hold tower information strings

    def tick(self, tower: 'str'):
        if tower is None:
            self.background.alpha = 0
            self.background.border_color = (255, 255, 255, 0)
            self.__text_surfaces = []
            return

        config = self.__scene.getTowerConfig().getTowerLevelConfig(tower, 1)
        self.background.alpha = 200
        self.background.border_color = (255, 255, 255, 255)
        self.background.x = pygame.mouse.get_pos()[0] + 10
        self.background.y = pygame.mouse.get_pos()[1] + 10
        self.background.rect.topleft = (self.background.x, self.background.y)

        # Prepare tower information
        self.__tower_info = [
            f"Name: {tower}",
            f"Damage: {config['damage']}",
            f"Range: {config['range']}",
            f"Attack Speed: {config['speed']}",
            f"Cost: {config['cost']}",
        ]

        # Render text surfaces
        font = self.__scene.getFont(14)
        self.__text_surfaces = [
            font.render(line, True, (255, 255, 255)).convert_alpha()
            for line in self.__tower_info
        ]

        # Adjust button size based on text
        line_height = font.get_linesize()
        padding = 10
        self.background.width = max(
            surface.get_width() for surface in self.__text_surfaces
        ) + 2 * padding
        self.background.height = line_height * len(self.__text_surfaces) + 2 * padding

    def draw(self):
        self.background.draw(self.__scene.getScreen())

        if self.__text_surfaces:
            padding = 10
            current_y = self.background.y + padding
            for text_surface in self.__text_surfaces:
                text_rect = text_surface.get_rect()
                text_rect.topleft = (
                    self.background.x + padding,
                    current_y
                )
                self.__scene.getScreen().blit(text_surface, text_rect)
                current_y += text_surface.get_height()

