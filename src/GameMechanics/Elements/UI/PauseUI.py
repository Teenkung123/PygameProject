from typing import TYPE_CHECKING

import pygame.event

from src.Utils.Events import PLAYER_EXIT
from src.Utils.Button import Button

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class PauseUI:
    def __init__(self, scene: 'GameScene'):
        self.__scene = scene
        self.__width = scene.getScreen().get_width()
        self.__height = scene.getScreen().get_height()
        self.__background = Button(x=0, y=0, w=scene.getScreen().get_width(), h=scene.getScreen().get_height(), color=(0, 0, 0), alpha=0)
        self.__pauseText = self.__scene.getFont(64).render("PAUSED", True, (255, 255, 255)).convert_alpha()
        self.__resumeButton = Button(
            x=self.__width // 2 - self.__width // 10,
            y=self.__height // 2,
            w=self.__width // 5,
            h=55,
            color=(255, 255, 255),
            hover_color=(200, 200, 200),
            text="Resume",
            border_width=3,
            border_color=(0, 0, 0),
            onLeftClick=lambda: self.__scene.getStageManager().pauseGame(False),
            visible=False
        )

        self.__exitButton = Button(
            x=self.__width // 2 - self.__width // 10,
            y=self.__height // 2 + 60,
            w=self.__width // 5,
            h=55,
            color=(200, 50, 50),
            hover_color=(255, 0, 0),
            text="Exit",
            hover_text="Are you Sure?",
            border_width=3,
            border_color=(0, 0, 0),
            onLeftClick=lambda: pygame.event.post(pygame.event.Event(PLAYER_EXIT)),
            visible=False
        )
        self.__fadeIn = 0.33
        self.__tick = 0

    def tick(self, dt: float):
        if self.__scene.getStageManager().isPaused():
            if self.__tick < self.__fadeIn:
                self.__tick += dt
            alpha255 = min(255, int(255 * self.__tick / self.__fadeIn))
            alpha128 = min(128, int(128 * self.__tick / self.__fadeIn))
            self.__background.alpha = alpha128
            self.__resumeButton.alpha = alpha255
            self.__exitButton.alpha = alpha255
            self.__pauseText.set_alpha(alpha255)
            self.__background.draw(self.__scene.getScreen())
            self.__resumeButton.draw(self.__scene.getScreen())
            self.__exitButton.draw(self.__scene.getScreen())
            self.__scene.getScreen().blit(self.__pauseText, (self.__width // 2 - self.__pauseText.get_width() // 2, self.__height // 2.5 - self.__pauseText.get_height() // 2))
            self.__resumeButton.visible = True
            self.__exitButton.visible = True
            return
        self.__tick = 0
        self.__resumeButton.visible = False
        self.__exitButton.visible = False
        self.__background.alpha = 0


    def handle_event(self, event):
        self.__resumeButton.handle_event(event)
        self.__exitButton.handle_event(event)
        return

    def getPauseTimeMultiplier(self) -> float:
        multiplier = 1 - (self.__tick / self.__fadeIn)
        multiplier = max(0.0, min(1.0, multiplier))  # Clamp between 0 and 1
        return multiplier
