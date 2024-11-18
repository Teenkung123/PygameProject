import logging
import os
import random

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Entities.Enemy import Enemy

import logging
import os
import random

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Entities.Enemy import Enemy

class Tower(pygame.sprite.Sprite):
    def __init__(self, gameScene: "GameScene", towerName: str):
        super().__init__()
        self._gameScene = gameScene
        self._rect = None
        self._gridSize = self._gameScene.getStageManager().getStageConfig().getGridSize()
        self._position = None
        self._truePosition = None
        self._isPlaced = False
        self._config = None
        self._level = 1
        self._damage = 0
        self._cooldown = 0
        self._speed = 0
        self._range = 0
        self._cost = 0
        self._image = None
        self._towerName = towerName  # Now passed as a parameter
        self._attack_type = "single_target"
        self._attack_priority = "first_enemy"
        self._debuffs = {}
        try:
            self._loadTowerConfig()
            self._loadImage()
        except Exception as e:
            logging.error(f"Error initializing Tower '{self._towerName}': {e}")
            raise

    def _loadTowerConfig(self):
        # Use the TowerConfig instance from the game scene
        tower_config_manager = self._gameScene.getTowerConfig()
        self._config = tower_config_manager.getTowerConfig(self._towerName)
        if not self._config:
            logging.error(f"Configuration for tower '{self._towerName}' not found.")
            raise ValueError(f"Configuration for tower '{self._towerName}' not found.")

        self._max_level = self._config.get("max_level", 1)
        self._attack_type = self._config.get("attack_type", "single_target")
        self._attack_priority = self._config.get("attack_priority", "first_enemy")
        self._updateStatsForLevel()

    def _updateStatsForLevel(self):
        level_config = self._config.get(str(self._level))
        if not level_config:
            logging.error(f"Level {self._level} config for tower '{self._towerName}' not found.")
            raise ValueError(f"Level {self._level} config for tower '{self._towerName}' not found.")

        self._damage = level_config.get("damage", 0)
        self._speed = level_config.get("speed", 0)
        self._range = level_config.get("range", 0)
        self._cost = level_config.get("cost", 0)
        self._debuffs = self._extractxDebuffs(level_config)
        # Additional attributes for specific attack types
        if self._attack_type == "AOE":
            self._blast_radius = level_config.get("blast_radius", 0)
            self._blast_damage = level_config.get("blast_damage", 0)

    # noinspection PyMethodMayBeStatic
    def _extractxDebuffs(self, level_config):
        debuffs = {}
        for key in ['slow_percent', 'slow_duration', 'slow_type',
                    'bleeding_damage', 'bleeding_duration', 'bleeding_type',
                    'burning_damage', 'burning_duration', 'add_gold_amount']:
            if key in level_config:
                debuffs[key] = level_config[key]
        return debuffs

    def tick(self, dt: float):
        if self._isPlaced:
            self._cooldown -= dt
            if self._cooldown <= 0:
                self.attack()

    def upgrade(self):
        if self._level < self._max_level:
            self._level += 1
            self._updateStatsForLevel()
            self._loadImage()
            return True
        return False

    def draw(self):
        screen = self._gameScene.getScreen()
        if self._isPlaced and self._image:
            center = (
                self._truePosition.x - self._image.get_width() // 2,
                self._truePosition.y - self._image.get_height() // 2
            )
            screen.blit(self._image, center)

    def place(self, position: tuple[int, int]):
        self._position = position
        self._truePosition = pygame.math.Vector2(
            position[0] * self._gridSize + self._gridSize // 2,
            position[1] * self._gridSize + self._gridSize // 2
        )
        self._isPlaced = True
        self._rect = self._image.get_rect(center=self._truePosition)
        logging.info(f"Placed tower '{self._towerName}' at {self._truePosition}")

    def attack(self):
        enemies_in_range = self._getEnemiesInRange()
        if not enemies_in_range:
            return

        if self._attack_type == 'around':
            for enemy in enemies_in_range:
                self._applyEffect(enemy)
            self._cooldown = self._speed
        else:
            target_enemy = self._selectTarget(enemies_in_range)
            if target_enemy:
                self._applyEffect(target_enemy)
                self._cooldown = self._speed

    def _getEnemiesInRange(self):
        enemies_in_range = []
        for enemy in self._gameScene.getWaveManager().getEnemies():
            enemy: "Enemy" = enemy
            enemyLoc = pygame.math.Vector2(enemy.rect.centerx, enemy.rect.centery)
            if enemyLoc.distance_to(self._truePosition) <= self._range * self._gridSize:
                enemies_in_range.append(enemy)
        return enemies_in_range

    def _selectTarget(self, enemies):
        if not enemies:
            return None

        # Prioritize enemies based on attack priority
        if self._attack_priority == "first_enemy":
            enemies.sort(key=lambda e: e.getProgress())
        elif self._attack_priority == "last_enemy":
            enemies.sort(key=lambda e: -e.getProgress())
        elif self._attack_priority == "lowest_health":
            enemies.sort(key=lambda e: e.getHealth())
        elif self._attack_priority == "highest_health":
            enemies.sort(key=lambda e: -e.getHealth())
        elif self._attack_priority == "random":
            random.shuffle(enemies)
        else:
            enemies.sort(key=lambda e: e.getProgress())

        return enemies[0]  # Return the first enemy after sorting

    def _applyEffect(self, target_enemy: "Enemy"):
        # Apply direct damage to the target enemy
        target_enemy.decreaseHealth(self._damage)

        # Apply debuffs to the target enemy
        self._applyDebuffs(target_enemy)

        # Handle blast damage to enemies around the target enemy
        if self._attack_type == "AOE":
            self._applyBlastDamage(target_enemy)

    def _applyBlastDamage(self, target_enemy: "Enemy"):
        enemies = self._gameScene.getWaveManager().getEnemies()
        target_position = pygame.math.Vector2(target_enemy.rect.centerx, target_enemy.rect.centery)
        for enemy in enemies:
            if enemy == target_enemy:
                continue  # Skip the target enemy
            enemy_position = pygame.math.Vector2(enemy.rect.centerx, enemy.rect.centery)
            distance = enemy_position.distance_to(target_position)
            if distance <= self._blast_radius * self._gridSize:
                enemy.decreaseHealth(self._blast_damage)
                # Apply debuffs to enemies hit by the blast
                self._applyDebuffs(enemy)

    def _applyDebuffs(self, enemy: "Enemy"):
        if 'slow_percent' in self._debuffs and 'slow_duration' in self._debuffs:
            key = f"slow_{self._towerName}"
            enemy.setSpeedMultiplier(key, self._debuffs['slow_percent'], self._debuffs['slow_duration'])
        if 'bleeding_damage' in self._debuffs and 'bleeding_duration' in self._debuffs:
            enemy.applyBleeding(self._debuffs['bleeding_damage'], self._debuffs['bleeding_duration'], self._towerName)
        if 'burning_damage' in self._debuffs and 'burning_duration' in self._debuffs:
            enemy.applyBurning(self._debuffs['burning_damage'], self._debuffs['burning_duration'], self._towerName)
        if 'add_gold_amount' in self._debuffs:
            self._gameScene.getCurrencyManager().deposit("gold", self._debuffs['add_gold_amount'])

    def _loadImage(self):
        # Get the image path for the current level
        level_config = self._config.get(str(self._level), {})
        image_path = level_config.get("image")

        if not image_path:
            # Fallback to the default image if level-specific image is not provided
            image_path = self._config.get("image")

        if not image_path:
            logging.error(f"No image specified for tower '{self._towerName}' at level {self._level}.")
            raise FileNotFoundError(f"No image specified for tower '{self._towerName}' at level {self._level}.")

        self._imagePath = os.path.join(
            self._gameScene.getProjectRoot(),
            image_path
        )
        self._imagePath = os.path.normpath(self._imagePath)
        if not os.path.exists(self._imagePath):
            raise FileNotFoundError(f"{self.__class__.__name__} image not found: {self._imagePath}")
        try:
            self._image = pygame.image.load(self._imagePath).convert_alpha()
            self._image = pygame.transform.scale(
                self._image,
                (int(self._gridSize * 0.8), int(self._gridSize * 0.8))
            )
            logging.debug(
                f"Loaded image for '{self.__class__.__name__}' at level {self._level} and scaled to ({self._gridSize}x{self._gridSize})."
            )
        except pygame.error as e:
            raise pygame.error(f"Error loading {self.__class__.__name__} image '{self._imagePath}': {e}")