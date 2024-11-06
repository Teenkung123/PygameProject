import logging
import sys
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Main import Main

class Screen:
    def __init__(self, main: 'Main'):
        try:
            screen_width = main.getConfig().getScreenWidth()
            screen_height = main.getConfig().getScreenHeight()
            self.__screen = pygame.display.set_mode(
                (screen_width, screen_height)
            )

            pygame.display.set_caption("Pygame Project")
            logging.info(f"Pygame initialized with screen size ({screen_width}x{screen_height}).")
        except pygame.error as e:
            logging.error(f"Error initializing Pygame display: {e}")
            sys.exit(1)

    def getScreen(self):
        return self.__screen
