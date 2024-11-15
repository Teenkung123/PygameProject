import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene


class EnemyReachEnd:

    @staticmethod
    def handle(event: 'pygame.event.Event', scene: 'GameScene'):
        scene.getUIManager().getHurtUI().hurt()
        scene.getPlayer().doDamage(event.enemy)
        pass
