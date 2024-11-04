import pygame
import logging
from Game.Entities.Enemy import Enemy

class WaveManager:
    def __init__(self, waves_config, enemies_config, path, grid_size, project_root, game_settings):
        """
        Initialize the WaveManager.

        :param waves_config: Dictionary containing wave information from stage config
        :param enemies_config: Dictionary containing enemy types and their configurations
        :param path: List of (x, y) tuples representing the walk path
        :param grid_size: Size of each grid cell
        :param project_root: Absolute path to the project root
        :param game_settings: Dictionary containing game-wide settings (e.g., player health, wave delay)
        """
        self.waves_config = waves_config
        self.enemies_config = enemies_config
        self.path = path
        self.grid_size = grid_size
        self.project_root = project_root

        # Game settings
        self.player_health = game_settings.get("player_health", 100)
        self.wave_delay = game_settings.get("wave_delay", 3.0)  # Seconds delay between waves

        self.current_wave = 0
        self.enemies_to_spawn = []
        self.spawn_timer = 0.0  # Time since last spawn
        self.spawn_interval = 0.0  # Spawn rate in seconds

        self.all_enemies = pygame.sprite.Group()

        self.wave_delay_timer = 0.0
        self.waiting_for_next_wave = False

        logging.info("WaveManager initialized.")

    def start_next_wave(self):
        self.current_wave += 1
        wave_key = str(self.current_wave)
        if wave_key in self.waves_config:
            wave_info = self.waves_config[wave_key]
            self.spawn_interval = wave_info.get("spawn_rate", 2.0)
            # Validate spawn_rate
            if not isinstance(self.spawn_interval, (int, float)) or self.spawn_interval <= 0:
                logging.warning(f"Invalid spawn_rate '{self.spawn_interval}' in wave {self.current_wave}. Using default 2.0.")
                self.spawn_interval = 2.0

            # Prepare list of enemies to spawn
            enemies = wave_info.get("enemies", {})
            if not enemies:
                logging.warning(f"No enemies defined for wave {self.current_wave}.")
            for enemy_type, count in enemies.items():
                if enemy_type not in self.enemies_config:
                    logging.error(f"Enemy type '{enemy_type}' not defined in enemies configuration.")
                    continue
                if not isinstance(count, int) or count < 0:
                    logging.warning(f"Invalid count '{count}' for enemy '{enemy_type}' in wave {self.current_wave}. Skipping.")
                    continue
                for _ in range(count):
                    self.enemies_to_spawn.append(enemy_type)
            logging.info(f"Wave {self.current_wave} started with {len(self.enemies_to_spawn)} enemies.")
        else:
            logging.info("All waves completed. Victory!")
            # Handle end of waves (e.g., display victory screen)

    def update(self, dt):
        """
        Update the WaveManager, spawning enemies as needed.

        :param dt: Delta time since last frame in seconds
        """
        if self.waiting_for_next_wave:
            self.wave_delay_timer += dt
            if self.wave_delay_timer >= self.wave_delay:
                self.waiting_for_next_wave = False
                self.wave_delay_timer = 0.0
                self.start_next_wave()
            return

        if self.current_wave == 0:
            self.start_next_wave()

        if self.spawn_timer >= self.spawn_interval and self.enemies_to_spawn:
            enemy_type = self.enemies_to_spawn.pop(0)
            try:
                enemy = Enemy(enemy_type, self.enemies_config, self.path, self.grid_size, self.project_root)
                self.all_enemies.add(enemy)
                logging.info(f"Spawned enemy: {enemy_type.capitalize()}")
            except FileNotFoundError as e:
                logging.error(e)
            except Exception as e:
                logging.error(f"Unexpected error spawning enemy '{enemy_type}': {e}")
            self.spawn_timer = 0.0

        if self.enemies_to_spawn:
            self.spawn_timer += dt

        # Update all enemies
        self.all_enemies.update(dt)

        # Check if wave is completed
        if not self.enemies_to_spawn and not self.all_enemies:
            self.waiting_for_next_wave = True
            self.wave_delay_timer = 0.0
            logging.info(f"Wave {self.current_wave} completed. Next wave in {self.wave_delay} seconds.")

    def draw(self, screen):
        """
        Draw all enemies on the screen.

        :param screen: Pygame screen surface
        """
        try:
            self.all_enemies.draw(screen)
        except Exception as e:
            logging.error(f"Error drawing enemies: {e}")

    def handle_enemy_reach_end(self, enemy):
        """
        Handle enemies reaching the end of the path.

        :param enemy: Enemy instance that reached the end
        """
        self.player_health -= enemy.damage
        logging.info(f"{enemy.enemy_type.capitalize()} reached the end. Player health: {self.player_health}")
        if self.player_health <= 0:
            logging.info("Player health depleted. Game Over!")
            pygame.event.post(pygame.event.Event(pygame.QUIT))  # Trigger game quit
