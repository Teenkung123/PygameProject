import logging

import pygame

from src.Scenes.Scene import Scene
from typing import TYPE_CHECKING

from dataclasses import dataclass,field
import src.Scenes.Constants as c
import src.Scenes.UIObjects as UI

if TYPE_CHECKING:
    import Main

class MainMenuScene(Scene):
    def __init__(self, main: 'Main'):
        super().__init__()
        self.__main = main
        self.__screen = main.getScreen()
        self.start_button = UI.Button(image=c.start_image, DISPLAY = self.__screen, rect = UI.box_genreator_from_center((959/2, 300),128,320))
        self.START = pygame.USEREVENT - 1
        #self.settings_button = UI.Button(image=None, DISPLAY = self.__screen, rect = UI.box_genreator_from_center((959/2, 500),50,300))
        #self.music_checkbox = UI.CheckBox(DISPLAY = self.__screen)
    
    def tick(self, dt: float):
        self.__screen.blit(c.main_menu_background, (0,0))
        UI.draw_text(self.__screen, "Tower Defense", c.TEXT_FONT_LARGE, c.BLACK, (100,100))
        if self.start_button.draw():
            print("Pressed")
            self.__main.setCurrentScene("game")
        #self.settings_button.draw2()
        #self.music_checkbox.draw()

    
    def reset(self):
        pass