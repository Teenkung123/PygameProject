import logging
import sys
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Main

class Screen:
    def __init__(self, main: 'Main'):
        self.__main = main
        self.__screen = None
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

    def draw(self, deltaTime: float):
        # Update wave manager and enemies
        try:
            self.__main.getWaveManager().update(deltaTime)
        except Exception as e:
            logging.error(f"Error updating WaveManager: {e}")

        # Draw the path and background
        try:
            self.__main.getStageManager().getBackground().draw()
            self.__main.getStageManager().getPath().draw()
        except Exception as e:
            logging.error(f"Error drawing StageManager: {e}")

        # Draw enemies
        try:
            self.__main.getWaveManager().draw(self.__screen)
        except Exception as e:
            logging.error(f"Error drawing enemies: {e}")

        self.__main.getUIManager().updateHealthBar()

        # Update the display
        try:
            pygame.display.flip()
        except Exception as e:
            logging.error(f"Error updating display: {e}")

    def getScreen(self):
        return self.__screen
