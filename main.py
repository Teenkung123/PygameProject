# main.py

import pygame
import sys
import os
import json
import logging
from config_loader import ConfigLoader
from Game.Manager.StageManager import StageManager
from Game.Manager.WaveManager import WaveManager

# Define the custom event type (ensure consistency with Enemy class)
ENEMY_REACHED_END = pygame.USEREVENT + 1

# Configure logging (optional if already configured in config_loader.py)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("game.log"),
        logging.StreamHandler()
    ]
)

class Main:
    def __init__(self):
        # Determine the project root directory
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        logging.info(f"Project Root: {self.project_root}")

        # Load main configuration
        self.__load_config()

        # Initialize Pygame
        pygame.init()
        try:
            screen_width = self.config.get("screen", {}).get("width", 800)
            screen_height = self.config.get("screen", {}).get("height", 600)
            self.screen = pygame.display.set_mode(
                (screen_width, screen_height)
            )
            pygame.display.set_caption("Pygame Project")
            logging.info(f"Pygame initialized with screen size ({screen_width}x{screen_height}).")
        except pygame.error as e:
            logging.error(f"Error initializing Pygame display: {e}")
            sys.exit(1)

        # Initialize StageManager
        try:
            self.stage_manager = StageManager(
                "default", self.config, self.screen, self.project_root
            )
        except Exception as e:
            logging.error(f"Failed to initialize StageManager: {e}")
            sys.exit(1)

        # Load enemies configuration
        self.enemies_config = self.__load_enemies_config()

        # Get the path
        self.path = self.stage_manager.get_path()
        if not self.path:
            logging.error("No valid path found. Exiting.")
            sys.exit(1)

        # Initialize WaveManager
        try:
            game_settings = self.config.get("game_settings", {})
            self.wave_manager = WaveManager(
                self.stage_manager.config.get("waves", {}),
                self.enemies_config,
                self.path,
                self.stage_manager.grid_size,
                self.project_root,
                game_settings
            )
        except Exception as e:
            logging.error(f"Failed to initialize WaveManager: {e}")
            sys.exit(1)

        # Retrieve player health for display purposes
        self.player_health = self.wave_manager.player_health

        # Set up fonts
        self.font = pygame.font.SysFont(None, 36)

    def __load_config(self):
        try:
            self.config = ConfigLoader().get_config()
            logging.info("Main configuration loaded successfully.")
        except FileNotFoundError as e:
            logging.error(e)
            sys.exit(1)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing main configuration: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error loading main configuration: {e}")
            sys.exit(1)

    def __load_enemies_config(self):
        enemies_config_path = os.path.join(self.project_root, "config", "enemies.json")
        enemies_config_path = os.path.normpath(enemies_config_path)
        logging.info(f"Loading Enemies Config from: {enemies_config_path}")

        if not os.path.exists(enemies_config_path):
            logging.error(f"Enemies configuration file not found: {enemies_config_path}")
            sys.exit(1)

        try:
            with open(enemies_config_path, "r") as f:
                enemies_config = json.load(f)
                logging.info("Enemies configuration loaded successfully.")
                return enemies_config
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing enemies configuration: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Unexpected error loading enemies configuration: {e}")
            sys.exit(1)

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60) / 1000.0  # Delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == ENEMY_REACHED_END:
                    enemy = event.enemy
                    self.wave_manager.handle_enemy_reach_end(enemy)
                    self.player_health = self.wave_manager.player_health
                    if self.player_health <= 0:
                        logging.info("Player has lost all health. Game Over!")
                        running = False

            # Update wave manager and enemies
            try:
                self.wave_manager.update(dt)
            except Exception as e:
                logging.error(f"Error updating WaveManager: {e}")

            # Draw the path and background
            try:
                self.stage_manager.draw()
            except Exception as e:
                logging.error(f"Error drawing StageManager: {e}")

            # Draw enemies
            try:
                self.wave_manager.draw(self.screen)
            except Exception as e:
                logging.error(f"Error drawing enemies: {e}")

            # Draw UI elements (e.g., player health)
            try:
                self.__draw_ui()
            except Exception as e:
                logging.error(f"Error drawing UI: {e}")

            # Update the display
            try:
                pygame.display.flip()
            except Exception as e:
                logging.error(f"Error updating display: {e}")

        # Display Game Over Screen
        self.__display_game_over()

        pygame.quit()
        sys.exit()

    def __draw_ui(self):
        # Display player health
        health_text = self.font.render(f"Health: {self.player_health}", True, (255, 255, 255))
        self.screen.blit(health_text, (10, 10))

    def __display_game_over(self):
        # Create a simple Game Over screen
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(self.config["screen"]["width"]//2, self.config["screen"]["height"]//2))
        self.screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        logging.info("Displayed Game Over screen.")

        # Wait for a few seconds before exiting
        pygame.time.delay(3000)

if __name__ == "__main__":
    Main().run()
