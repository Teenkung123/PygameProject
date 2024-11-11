from typing import TYPE_CHECKING

import pygame


if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Entities.Enemy import Enemy


class EnemyHealthBar:
    def __init__(self, gameScene: 'GameScene'):
        self.__main = gameScene

    def display(self):
        for e in self.__main.getWaveManager().getEnemies():
            enemy: 'Enemy' = e
            width = enemy.rect.width
            if enemy.getHealth() == enemy.getMaxHealth():
                continue

            health_ratio = enemy.getHealth() / enemy.getMaxHealth()
            current_health_width = max(int(width * health_ratio), 1)

            if enemy.getTotalSpeedMultiplier() > 0:
                currentHealth = self.__main.getGradientUtils().get_horizontal_gradient(current_health_width, 5, [(0, 0, 128), (0, 0, 255)])
            else:
                currentHealth = self.__main.getGradientUtils().get_horizontal_gradient(current_health_width, 5, [(0, 128, 0), (0, 255, 0)])
            self.__main.getScreen().blit(currentHealth, (enemy.rect.x, enemy.rect.top - 10))
            pygame.draw.rect(self.__main.getScreen(), (0, 0, 0), pygame.Rect(enemy.rect.x, enemy.rect.top - 10, width, 7), 2)
