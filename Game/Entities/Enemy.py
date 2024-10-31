# Game/Entities/Enemy.py

import pygame
import os
import math
import logging

# Define a custom event type
ENEMY_REACHED_END = pygame.USEREVENT + 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, config, path, grid_size, project_root):
        super().__init__()
        self.enemy_type = enemy_type
        self.config = config.get(enemy_type, {})
        self.path = path  # List of (x, y) tuples
        self.grid_size = grid_size
        self.project_root = project_root

        # Validate enemy configuration
        if not self.config:
            logging.error(f"No configuration found for enemy type '{enemy_type}'.")
            raise ValueError(f"No configuration found for enemy type '{enemy_type}'.")

        # Load image
        image_rel_path = self.config.get("image", "")
        if not image_rel_path:
            logging.error(f"No image path specified for enemy type '{enemy_type}'.")
            raise ValueError(f"Enemy type '{enemy_type}' must have an 'image' path.")

        image_path = os.path.join(project_root, image_rel_path)
        image_path = os.path.normpath(image_path)
        if not os.path.exists(image_path):
            logging.error(f"Enemy image not found: {image_path}")
            raise FileNotFoundError(f"Enemy image not found: {image_path}")

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            # Scale image to grid size
            self.image = pygame.transform.scale(
                self.image,
                (self.grid_size, self.grid_size)
            )
            logging.info(f"Loaded image for '{enemy_type}' and scaled to ({self.grid_size}x{self.grid_size}).")
        except pygame.error as e:
            logging.error(f"Error loading enemy image '{image_path}': {e}")
            raise

        self.rect = self.image.get_rect()

        # Initialize position at the first node
        try:
            start_x, start_y = self.path[0]
            self.pos = pygame.math.Vector2(start_x * self.grid_size + (self.grid_size*0.5), start_y * self.grid_size + (self.grid_size*0.5))
            self.rect.center = self.pos
            logging.debug(f"Initialized '{enemy_type}' at position ({self.pos.x}, {self.pos.y}).")
        except IndexError:
            logging.error("Path is empty. Cannot initialize enemy position.")
            raise
        except ValueError:
            logging.error("Invalid path coordinates. Must be integers.")
            raise

        # Movement
        self.current_node = 0
        self.speed = self.config.get("speed", 100)  # Pixels per second
        if not isinstance(self.speed, (int, float)) or self.speed <= 0:
            logging.warning(f"Invalid speed '{self.speed}' for '{enemy_type}'. Using default speed 100.")
            self.speed = 100

        # Health and damage
        self.health = self.config.get("health", 100)
        self.damage = self.config.get("damage", 10)
        if not isinstance(self.health, int) or self.health <= 0:
            logging.warning(f"Invalid health '{self.health}' for '{enemy_type}'. Using default health 100.")
            self.health = 100
        if not isinstance(self.damage, int) or self.damage < 0:
            logging.warning(f"Invalid damage '{self.damage}' for '{enemy_type}'. Using default damage 10.")
            self.damage = 10

    def update(self, dt):
        if self.current_node >= len(self.path) - 1:
            # Reached the end
            self.kill()  # Remove from sprite groups
            # Emit custom event
            pygame.event.post(pygame.event.Event(ENEMY_REACHED_END, {"enemy": self}))
            logging.info(f"{self.enemy_type.capitalize()} reached the end.")
            return

        target_x, target_y = self.path[self.current_node + 1]
        target_pos = pygame.math.Vector2(target_x * self.grid_size + (self.grid_size*0.5), target_y * self.grid_size + (self.grid_size*0.5))

        direction = target_pos - self.pos
        distance = direction.length()

        if distance == 0:
            self.current_node += 1
            return

        direction = direction.normalize()

        # Move towards target
        movement = direction * self.speed * dt
        if movement.length() >= distance:
            self.pos = target_pos
            self.current_node += 1
        else:
            self.pos += movement

        self.rect.center = self.pos

    def draw(self, screen):
        try:
            screen.blit(self.image, self.rect.topleft)
        except Exception as e:
            logging.error(f"Error drawing enemy '{self.enemy_type}': {e}")
