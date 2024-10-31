# Game/Manager/StageManager.py

import json
import os
import pygame
import logging

from Game.Manager.WaveManager import WaveManager  # Ensure this module exists


class StageManager:
    def __init__(self, stage, config, screen, project_root):
        """
        Initialize the StageManager.

        :param stage: Name of the stage (e.g., "default")
        :param config: Main configuration dictionary
        :param screen: Pygame screen surface
        :param project_root: Absolute path to the project root directory
        """
        self.main_config = config
        self.screen = screen
        self.project_root = project_root
        logging.info(f"StageManager Initialized with Project Root: {self.project_root}")

        # Load stage-specific config
        config_path = os.path.join(self.project_root, "config", "stage", f"{stage}.json")
        config_path = os.path.normpath(config_path)  # Normalize the path
        logging.info(f"Loading Stage Config from: {config_path}")

        if not os.path.exists(config_path):
            logging.error(f"Stage configuration file not found: {config_path}")
            raise FileNotFoundError(f"Stage configuration file not found: {config_path}")

        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
                logging.info(f"Stage configuration '{stage}' loaded successfully.")
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing stage configuration: {e}")
            raise

        # Calculate grid size based on screen dimensions
        screen_width = self.main_config.get("screen", {}).get("width", 800)
        screen_height = self.main_config.get("screen", {}).get("height", 600)
        grid_size = self.config.get("grid_size", 21)

        if grid_size <= 0:
            logging.warning(f"Invalid grid_size '{grid_size}'. Setting to default value 21.")
            grid_size = 21

        self.grid_size = min(screen_width // grid_size, screen_height // grid_size)
        logging.info(f"Calculated Grid Size: {self.grid_size}")

        # Load and scale the background image
        background_relative = self.config.get("background", "")
        if background_relative:
            background_path = os.path.join(os.path.dirname(config_path), background_relative)
            background_path = os.path.normpath(background_path)
            logging.info(f"Background Image Path: {background_path}")

            if os.path.exists(background_path):
                try:
                    self.background_img = pygame.image.load(background_path).convert()
                    self.background_img = pygame.transform.scale(
                        self.background_img,
                        (screen_width, screen_height)
                    )
                    logging.info("Background image loaded and scaled.")
                except pygame.error as e:
                    logging.error(f"Error loading background image: {e}")
                    self.background_img = None
            else:
                logging.error(f"Background image not found: {background_path}")
                self.background_img = None
        else:
            self.background_img = None

        # Load and scale the path image once
        path_image_relative = self.config.get("path", "")
        if not path_image_relative:
            logging.error("No 'path' specified in stage configuration.")
            raise ValueError("Stage configuration must include a 'path' to the path image.")

        path_image_path = os.path.join(os.path.dirname(config_path), path_image_relative)
        path_image_path = os.path.normpath(path_image_path)
        logging.info(f"Path Image Path: {path_image_path}")

        if not os.path.exists(path_image_path):
            logging.error(f"Path image not found: {path_image_path}")
            raise FileNotFoundError(f"Path image not found: {path_image_path}")

        try:
            self.path_img = pygame.image.load(path_image_path).convert_alpha()
            self.path_img = pygame.transform.scale(self.path_img, (self.grid_size, self.grid_size))
            logging.info(f"Path image loaded and scaled to: {self.grid_size}x{self.grid_size}")
        except pygame.error as e:
            logging.error(f"Error loading path image: {e}")
            raise

        # Create a separate surface for the path
        screen_width_px = screen_width
        screen_height_px = screen_height
        try:
            self.path_surface = pygame.Surface((screen_width_px, screen_height_px), pygame.SRCALPHA)
            self.__draw_path()
        except Exception as e:
            logging.error(f"Error creating path surface: {e}")
            raise

    def __draw_path(self):
        path = self.config.get("walk_path", [])
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
        x1, y1 = start
        x2, y2 = end

        if x1 == x2:
            # Vertical movement
            step = 1 if y2 > y1 else -1
            for y in range(y1, y2 + step, step):
                try:
                    self.path_surface.blit(self.path_img, (x1 * self.grid_size, y * self.grid_size))
                    logging.debug(f"Drew path at ({x1}, {y})")
                except Exception as e:
                    logging.error(f"Error drawing path at ({x1}, {y}): {e}")
        elif y1 == y2:
            # Horizontal movement
            step = 1 if x2 > x1 else -1
            for x in range(x1, x2 + step, step):
                try:
                    self.path_surface.blit(self.path_img, (x * self.grid_size, y1 * self.grid_size))
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
        path = self.config.get("walk_path", [])
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
            if self.background_img:
                self.screen.blit(self.background_img, (0, 0))
            else:
                bg_color = self.main_config.get("game_settings", {}).get("background_color", [0, 0, 0])
                self.screen.fill(bg_color)  # Fallback to configured background color or black

            self.screen.blit(self.path_surface, (0, 0))
        except Exception as e:
            logging.error(f"Error during StageManager draw: {e}")
