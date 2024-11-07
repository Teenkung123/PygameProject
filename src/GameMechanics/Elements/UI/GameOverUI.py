import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class GameOverUI:
    def __init__(self, gameScene: 'GameScene'):
        self.__main = gameScene

    def display(self):
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(
            center=(
                self.__main.getConfig().getScreenWidth() // 2,
                self.__main.getConfig().getScreenHeight() // 2
            )
        )
        self.__main.getScreen().blit(game_over_text, text_rect)

