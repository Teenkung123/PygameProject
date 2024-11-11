import logging
import os.path
from typing import TYPE_CHECKING

import pygame
from pygame import Vector2

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene


class InventoryUI:
    def __init__(self, gameScene: 'GameScene'):
        self.__main = gameScene
        self.__font = gameScene.getFont(12)
        self.__load_image()
        self.__define_slot_positions()
        self.__button_rects = []
        self.__init_button_area()

    def __load_image(self):
        path = os.path.join(self.__main.getProjectRoot(), "config", "images", "hotbar.png")
        image_path = os.path.normpath(path)
        if not os.path.exists(image_path):
            logging.error(f"InventoryUI image not found: {image_path}")
            raise FileNotFoundError(f"InventoryUI image not found: {image_path}")

        original_image = pygame.image.load(image_path)
        original_width, original_height = original_image.get_size()

        # Define the desired new width
        self.__new_width = 584
        self.__scaling_factor = self.__new_width / original_width
        self.__new_height = int(original_height * self.__scaling_factor)

        # Scale the image
        self.__image = pygame.transform.scale(original_image, (self.__new_width, self.__new_height))
        logging.debug(
            f"Hotbar image scaled by factor {self.__scaling_factor} to size ({self.__new_width}, {self.__new_height})")

    def __define_slot_positions(self):
        """
        Define the original slot positions relative to the unscaled hotbar image.
        These positions will be scaled based on the image scaling factor.
        """
        self.__original_slot_positions = [
            Vector2(13, 12),
            Vector2(92, 12),
            Vector2(172, 12),
            Vector2(252, 12),
            Vector2(332, 12),
            Vector2(412, 12),
            Vector2(492, 12),
            Vector2(572, 12),
            Vector2(652, 12)
        ]
        logging.debug("Original slot positions defined.")

    def __init_button_area(self):
        """
        Initialize button rectangles based on the scaled slot positions and scaled button sizes.
        """
        self.__button_rects = []
        scaled_button_size = 64 * self.__scaling_factor  # Scale button size if necessary
        for idx, pos in enumerate(self.__original_slot_positions):
            scaled_pos = pos * self.__scaling_factor
            rect = pygame.Rect(scaled_pos.x, scaled_pos.y, scaled_button_size, scaled_button_size)
            self.__button_rects.append(rect)
            logging.debug(f"Button {idx} rect set to {rect}")
        logging.info(f"Initialized {len(self.__button_rects)} button areas.")

    def display(self):
        """
        Render the hotbar and the button overlays on the screen.
        """
        screen_width = self.__main.getConfig().getScreenWidth()
        screen = self.__main.getScreen()

        # Calculate hotbar position
        x_position = (screen_width - self.__new_width) // 2
        y_position = -4  # Existing y-coordinate adjustment
        screen.blit(self.__image, (x_position, y_position))
        logging.debug(f"Hotbar image blitted at ({x_position}, {y_position})")

        # Draw a red border around each button area, offset by hotbar position
        for idx, rect in enumerate(self.__button_rects):
            absolute_rect = rect.move(x_position, y_position)
            pygame.draw.rect(screen, (255, 0, 0), absolute_rect, 2)  # 2-pixel border thickness
            logging.debug(f"Button {idx} drawn at {absolute_rect}")

    def handle_event(self, event):
        """
        Handle mouse click events to detect button interactions.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            logging.debug(f"Mouse click detected at {mouse_pos}")

            screen_width = self.__main.getConfig().getScreenWidth()
            x_position = (screen_width - self.__new_width) // 2
            y_position = -4  # Same y-coordinate as display

            for index, rect in enumerate(self.__button_rects):
                absolute_rect = rect.move(x_position, y_position)
                if absolute_rect.collidepoint(mouse_pos):
                    self.on_button_click(index)
                    logging.info(f"Button {index} clicked at {mouse_pos}")

    def on_button_click(self, index):
        """
        Handle the logic when a button is clicked.
        """
        logging.info(f"Button {index} clicked")
        # Implement the desired action for the clicked button here
        # Example: self.__main.select_inventory_slot(index)
