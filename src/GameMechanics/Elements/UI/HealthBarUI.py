from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class HealthBarUI:
    def __init__(self, gameScene: 'GameScene', font):
        self.__main = gameScene
        self.__font = font

    def display(self):
        health_text = self.__font.render(f"Health: {self.__main.getPlayer().getHealth()}", True, (255, 255, 255))
        self.__main.getScreen().blit(health_text, (10, 10))