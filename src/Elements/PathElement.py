import logging
import os
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Main import Main
    from Manager import StageConfig

class PathElement:
    def __init__(self, stageConfig: 'StageConfig', main: 'Main', screen: 'pygame.Surface'):
        self.__stageConfig = stageConfig
        self.__main = main
        self.__screen = screen
        self.__grid_size = self.__stageConfig.getGridSize()
        self.__loadPathImage()

    def __loadPathImage(self):
        # Load and scale the path image once
        path_image_relative = self.__stageConfig.getPathImage()
        if not path_image_relative:
            logging.error("No 'path' specified in stage configuration.")
            raise ValueError("Stage configuration must include a 'path' to the path image.")

        path_image_path = os.path.join(self.__main.getProjectRoot(), path_image_relative)
        path_image_path = os.path.normpath(path_image_path)
        logging.info(f"Path Image Path: {path_image_path}")

        if not os.path.exists(path_image_path):
            logging.error(f"Path image not found: {path_image_path}")
            raise FileNotFoundError(f"Path image not found: {path_image_path}")

        try:
            self.path_img = pygame.image.load(path_image_path).convert_alpha()
            self.path_img = pygame.transform.scale(self.path_img, (self.__grid_size, self.__grid_size))
            logging.info(f"Path image loaded and scaled to: {self.__grid_size}x{self.__grid_size}")
        except pygame.error as e:
            logging.error(f"Error loading path image: {e}")
            raise

        # Create a separate surface for the path
        try:
            self.path_surface = pygame.Surface((self.__screen.get_width(), self.__screen.get_height()), pygame.SRCALPHA)
            self.__draw_path()
            logging.info("Path surface created and path drawn successfully.")
        except Exception as e:
            logging.error(f"Error creating path surface: {e}")
            raise

    def __draw_path(self):
        """
        Draw the walk path on the path surface.
        """
        path = self.__stageConfig.getConfig().get("walk_path", [])
        if not path:
            logging.warning("No walk_path defined in the stage configuration.")
            return  # No path to draw

        # Convert all path coordinates to tuples of integers
        try:
            path_coords = [tuple(map(int, coord.split(','))) for coord in path]
            logging.info(f"Walk Path Coordinates: {path_coords}")
        except ValueError as e:
            logging.error(f"Error parsing walk_path coordinates: {e}")
            raise

        # Iterate through consecutive pairs of coordinates
        for i in range(len(path_coords) - 1):
            start = path_coords[i]
            end = path_coords[i + 1]
            self.__draw_segment(start, end)

    def __draw_segment(self, start, end):
        """
        Draw a segment of the path between two points.

        :param start: Tuple (x1, y1)
        :param end: Tuple (x2, y2)
        """
        x1, y1 = start
        x2, y2 = end

        if x1 == x2:
            # Vertical movement
            step = 1 if y2 > y1 else -1
            for y in range(y1, y2 + step, step):
                try:
                    self.path_surface.blit(self.path_img, (x1 * self.__grid_size, y * self.__grid_size))
                    logging.debug(f"Drew path at ({x1}, {y})")
                except Exception as e:
                    logging.error(f"Error drawing path at ({x1}, {y}): {e}")
        elif y1 == y2:
            # Horizontal movement
            step = 1 if x2 > x1 else -1
            for x in range(x1, x2 + step, step):
                try:
                    self.path_surface.blit(self.path_img, (x * self.__grid_size, y1 * self.__grid_size))
                    logging.debug(f"Drew path at ({x}, {y1})")
                except Exception as e:
                    logging.error(f"Error drawing path at ({x}, {y1}): {e}")
        else:
            # Diagonal or unsupported movement
            logging.warning(
                f"Diagonal movement detected from {start} to {end}. Splitting into horizontal and vertical segments.")
            # First, move horizontally to x2
            self.__draw_segment((x1, y1), (x2, y1))
            # Then, move vertically to y2
            self.__draw_segment((x2, y1), (x2, y2))

    def get_path(self):
        """
        Return the walk path as a list of (x, y) tuples.
        """
        path = self.__stageConfig.getConfig().get("walk_path", [])
        if not path:
            logging.warning("No walk_path defined in the stage configuration.")
            return []
        try:
            path_coords = [tuple(map(int, coord.split(','))) for coord in path]
            logging.info(f"Walk Path Coordinates: {path_coords}")
            return path_coords
        except ValueError as e:
            logging.error(f"Error parsing walk_path coordinates: {e}")
            return []

    def draw(self):
        """
        Blit the background and path surfaces onto the main screen.
        """
        try:
            screen = self.__main.getScreen()
            screen.blit(self.path_surface, (0, 0))
        except Exception as e:
            logging.error(f"Error during StageManager draw: {e}")

