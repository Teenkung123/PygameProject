import logging
import os.path
from typing import TYPE_CHECKING

import pygame

from src import Events
from src.Events import ENEMY_REACHED_END

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class Enemy(pygame.sprite.Sprite):
    def __init__(self, gameScene: 'GameScene', enemyType: str):
        super().__init__()
        self.__position = None
        self.__main = gameScene
        self.__type = enemyType
        self.__config = gameScene.getEnemyConfig().getConfig()[enemyType]
        self.__walkPath = gameScene.getStageManager().getStageConfig().getWalkPath()
        self.__gridSize = gameScene.getStageManager().getStageConfig().getGridSize()
        self.__speedMultipliers = {}
        self.__sizeMultiplier = 0.8
        self.__currentNode = 0
        self.__maxHealth = 100
        self.__health = 100
        self.__damage = 10
        self.__speed = 100
        self.__reward = 10
        self.image = None
        self.__loadEnemy()
        self.__total_path_length = self.__calculate_total_path_length()
        self.__effects = []

    def __loadEnemy(self):
        if not self.__config:
            logging.error(f"No configuration found for enemy type '{self.__type}'.")
            raise ValueError(f"No configuration found for enemy type '{self.__type}'.")

        self.__speed = self.__config.get("speed", 100)
        self.__damage = self.__config.get("damage", 10)
        self.__maxHealth = self.__config.get("health", 100)
        self.__reward = self.__config.get("reward", 10)
        self.__health = self.__maxHealth
        self.__loadImage()

    def __loadImage(self):
        self.__imagePath = os.path.join(self.__main.getProjectRoot(), self.__config["image"])
        self.__imagePath = os.path.normpath(self.__imagePath)
        if not os.path.exists(self.__imagePath):
            raise FileNotFoundError(f"Enemy image not found: {self.__imagePath}")
        try:
            self.image = pygame.image.load(self.__imagePath).convert_alpha()
            grid_size = self.__main.getStageManager().getStageConfig().getGridSize()
            new_size = int(grid_size * self.__sizeMultiplier)
            self.image = pygame.transform.scale(self.image, (new_size, new_size))
            logging.debug(f"Loaded image for '{self.__type}' and scaled to ({new_size}x{new_size}).")
        except pygame.error as e:
            raise pygame.error(f"Error loading enemy image '{self.__imagePath}': {e}")

        self.rect = self.image.get_rect()

    def spawn(self):
        try:
            x, y = map(int, self.__walkPath[0].split(","))
            self.__position = pygame.math.Vector2(
                x * self.__gridSize + (self.__gridSize / 2),
                y * self.__gridSize + (self.__gridSize / 2)
            )
            self.rect.center = self.__position
            logging.debug(f"Enemy spawned at {self.__position}.")
        except IndexError:
            logging.error("No path defined for enemy.")
            raise

    def update(self, deltaTime: float):
        if not self.alive():
            return

        # Update speed multipliers durations and remove expired ones
        self.__update_speed_multipliers(deltaTime)
        self.__updateEffects(deltaTime)

        if self.__currentNode >= len(self.__walkPath) - 1:
            self.kill()
            pygame.event.post(pygame.event.Event(ENEMY_REACHED_END, enemy=self))
            logging.info("Enemy reached the end.")
            return

        x, y = map(int, self.__walkPath[self.__currentNode + 1].split(","))
        target = pygame.math.Vector2(
            x * self.__gridSize + (self.__gridSize / 2),
            y * self.__gridSize + (self.__gridSize / 2)
        )

        direction = target - self.__position
        distance = direction.length()

        if distance == 0:
            self.__currentNode += 1
            return
        direction = direction.normalize()

        # Adjusted speed calculation
        total_speed_multiplier = sum([effect['multiplier'] for effect in self.__speedMultipliers.values()])
        total_speed_multiplier = min(total_speed_multiplier, 1)  # Cap at 1.0 (100% slow)
        speed_multiplier = 1.0 - total_speed_multiplier  # Remaining speed percentage
        speed_multiplier = max(speed_multiplier, 0.0)  # Ensure speed doesn't go negative

        movement = direction * (self.__speed * speed_multiplier) * (deltaTime * self.__main.getUIManager().pauseUI.getPauseTimeMultiplier())
        if movement.length() > distance:
            self.__position = target
            self.__currentNode += 1
        else:
            self.__position += movement

        self.rect.center = self.__position

    def __update_speed_multipliers(self, deltaTime: float):
        expired_effects = []
        for key, effect in self.__speedMultipliers.items():
            effect['duration'] -= deltaTime * 1000  # Convert deltaTime to milliseconds
            if effect['duration'] <= 0:
                expired_effects.append(key)
        for key in expired_effects:
            del self.__speedMultipliers[key]

    def __updateEffects(self, deltaTime: float):
        expired_effects = []
        for effect in self.__effects:
            effect['duration'] -= deltaTime * 1000  # Convert deltaTime to milliseconds
            effect['time_since_last_application'] += deltaTime
            if effect['duration'] <= 0:
                expired_effects.append(effect)
                continue
            while effect['time_since_last_application'] >= 0.5:
                self.decreaseHealth(effect['damage'])
                effect['time_since_last_application'] -= 0.5
        for effect in expired_effects:
            self.__effects.remove(effect)

    def applyBleeding(self, damage, duration, tower_type):
        existing_effect = next((e for e in self.__effects if e['type'] == 'bleeding' and e['tower_type'] == tower_type), None)
        if existing_effect:
            existing_effect['duration'] = duration
        else:
            self.__effects.append({
                'type': 'bleeding',
                'tower_type': tower_type,
                'damage': damage,
                'duration': duration,
                'time_since_last_application': 0.0
            })

    def applyBurning(self, damage, duration, tower_type):
        existing_effect = next((e for e in self.__effects if e['type'] == 'burning' and e['tower_type'] == tower_type), None)
        if existing_effect:
            existing_effect['duration'] = duration
        else:
            self.__effects.append({
                'type': 'burning',
                'tower_type': tower_type,
                'damage': damage,
                'duration': duration,
                'time_since_last_application': 0.0
            })

    def setSpeedMultiplier(self, key: str, multiplier: float, duration_ms: float):
        if multiplier < 0 or multiplier > 1:
            raise ValueError("Multiplier should be between 0 and 1.")
        # If the key already exists, reset the duration
        if key in self.__speedMultipliers:
            self.__speedMultipliers[key]['duration'] = duration_ms
        else:
            self.__speedMultipliers[key] = {'multiplier': multiplier, 'duration': duration_ms}

    def draw(self):
        try:
            # Blit the enemy image onto the screen
            self.__main.getScreen().blit(self.image, self.rect)
        except Exception as e:
            logging.error(f"Error drawing enemy: {e}")

    def isSlowed(self):
        total_speed_multiplier = sum([effect['multiplier'] for effect in self.__speedMultipliers.values()])
        return total_speed_multiplier > 0

    def getTotalSpeedMultiplier(self):
        return sum([effect['multiplier'] for effect in self.__speedMultipliers.values()])

    def getSpeedMultiplier(self, key: str):
        return self.__speedMultipliers[key]['multiplier']

    def removeSpeedMultiplier(self, key: str):
        if key in self.__speedMultipliers:
            del self.__speedMultipliers[key]

    def killEnemy(self):
        pygame.event.post(pygame.event.Event(Events.ENEMY_KILLED, enemy=self))
        self.kill()

    def getPosition(self):
        return self.__position

    def getRect(self):
        return self.rect

    def getDamage(self):
        return self.__damage

    def getHealth(self):
        return self.__health

    def getMaxHealth(self):
        return self.__maxHealth

    def getSpeed(self):
        return self.__speed

    def setSpeed(self, speed: int):
        self.__speed = speed

    def setHealth(self, health: int):
        self.__health = health
        if self.__health <= 0:
            self.killEnemy()

    def decreaseHealth(self, damage: int):
        self.__health -= damage
        if self.__health <= 0:
            self.killEnemy()

    def isAlive(self):
        return self.__health > 0 and self.alive()

    def getType(self):
        return self.__type

    def setReward(self, reward: int):
        self.__reward = reward

    def getReward(self):
        return self.__reward

    def __calculate_total_path_length(self):
        # Calculate the total length of the path for progress calculation
        total_length = 0
        for i in range(len(self.__walkPath) - 1):
            current_node_coords = list(map(int, self.__walkPath[i].split(",")))
            next_node_coords = list(map(int, self.__walkPath[i + 1].split(",")))
            current_node = pygame.math.Vector2(current_node_coords[0], current_node_coords[1])
            next_node = pygame.math.Vector2(next_node_coords[0], next_node_coords[1])
            total_length += current_node.distance_to(next_node)
        return total_length

    def getProgress(self):
        # Calculate how far the enemy has progressed along the path
        progress = 0
        for i in range(self.__currentNode):
            current_node_coords = list(map(int, self.__walkPath[i].split(",")))
            next_node_coords = list(map(int, self.__walkPath[i + 1].split(",")))
            current_node = pygame.math.Vector2(current_node_coords[0], current_node_coords[1])
            next_node = pygame.math.Vector2(next_node_coords[0], next_node_coords[1])
            progress += current_node.distance_to(next_node)
        # Add the distance from current position to next node
        if self.__currentNode < len(self.__walkPath) - 1:
            next_node_coords = list(map(int, self.__walkPath[self.__currentNode + 1].split(",")))
            next_node = pygame.math.Vector2(next_node_coords[0], next_node_coords[1])
            progress += self.__position.distance_to(next_node)
        return progress / self.__total_path_length
