import pygame

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.GameMechanics.Entities.Enemy import Enemy
    from src.Scenes.GameScene import GameScene
    from Game import Main


def handle(event, scene: 'GameScene', main: 'Main'):
    enemy: Enemy =  event.enemy
    scene.getCurrencyManager().deposit("gold", enemy.getReward())
    pass