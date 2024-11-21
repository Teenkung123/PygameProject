import pygame

from src.Utils.Button import Button
from src.Scenes.Scene import Scene
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Main

class MainMenuScene(Scene):
    def __init__(self, main: 'Main'):
        super().__init__()
        self.__main = main
        self.__screen: pygame.Surface = main.getScreen()

        bg = pygame.transform.scale(pygame.image.load("config/images/Home/foreground.png"), (self.__screen.get_width(), self.__screen.get_height()))
        self.background: Button = Button(
            image=bg,
            x=0, y=0, w=self.__screen.get_width(), h=self.__screen.get_height(),
            visible=True,
            color=(0, 0, 0),
            alpha=200
        )

        bw, bh = 250, 100
        img = pygame.transform.scale(pygame.image.load("config/images/Home/start.png"), (bw, bh))
        self.startBtn: Button = Button(
            image=img,
            x=(self.__screen.get_width() / 2) - (bw / 2),
            y=(self.__screen.get_height() / 2) - (bh / 2),
            w=bw,
            h=bh,
            visible=True,
            onLeftClick=lambda: self.__main.setCurrentScene("game")
        )

        self.title_text = "Tower Defense"
        self.title_font = main.getFont(72)
        self.title_color = (255, 255, 255)

        self.title_surface = self.title_font.render(self.title_text, True, self.title_color)

        # Get the rectangle of the text surface
        self.title_rect = self.title_surface.get_rect()

        # Calculate center position with Y offset
        self.title_rect.centerx = self.__screen.get_width() / 2
        self.title_rect.centery = (self.__screen.get_height() / 2) - 150  # Y offset of -150

    def tick(self, dt: float):
        # Draw the main menu background
        self.__screen.blit(self.__screen, (0, 0))

        # Draw the semi-transparent background overlay
        self.background.draw(self.__screen)

        # Draw the Start Button
        self.startBtn.draw(self.__screen)

        # Draw the Title Text
        self.__screen.blit(self.title_surface, self.title_rect)