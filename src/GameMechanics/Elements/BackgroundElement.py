import logging
import os
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameMechanics.StageConfig import StageConfig
    from ConfigLoader import ConfigLoader

class BackgroundElement:
    def __init__(self, stageConfig: 'StageConfig', mainConfig: 'ConfigLoader', screen: 'pygame.Surface'):
        """
        Initialize the Background.

        :param stageConfig: Instance of StageConfig containing stage-specific configurations
        :param mainConfig: Instance of ConfigLoader containing main configurations
        :param screen: Pygame screen surface
        """
        self.background_img = None
        self.stage_config = stageConfig
        self.main_config = mainConfig
        self.screen = screen
        self.drawBackground()

    def drawBackground(self):
        """
        Load and scale the background image based on the stage configuration.
        """
        background_image = self.stage_config.getBackgroundImage()
        background_path = os.path.join(self.main_config.getProjectRoot(), background_image)
        background_path = os.path.normpath(background_path)
        logging.info(f"Background Image Path: {background_path}")

        if os.path.exists(background_path):
            try:
                self.background_img = pygame.image.load(background_path).convert_alpha()
                self.background_img = pygame.transform.scale(
                    self.background_img,
                    (self.main_config.getScreenWidth(), self.main_config.getScreenHeight())
                )
                logging.info("Background image loaded and scaled.")
            except pygame.error as e:
                logging.error(f"Error loading background image: {e}")
                self.background_img = None
        else:
            logging.error(f"Background image not found: {background_path}")
            self.background_img = None
        self.draw()

    def draw(self):
        """
        Draw the background onto the screen.
        """
        try:
            if self.background_img:
                self.screen.blit(self.background_img, (0, 0))
            else:
                bg_color = self.stage_config.getConfig().get("game_settings", {}).get("background_color", [0, 0, 0])
                self.screen.fill(bg_color)  # Fallback to configured background color or black
        except Exception as e:
            logging.error(f"Error drawing background: {e}")
