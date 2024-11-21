from typing import TYPE_CHECKING

import pygame.image

from src.Utils.Button import Button

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class WaveChangeUI:
    def __init__(self, scene: 'GameScene'):
        self.__scene = scene
        self.__width = scene.getScreen().get_width()
        self.__height = scene.getScreen().get_height()
        self.__background = Button(x=0, y=0, w=scene.getScreen().get_width(), h=scene.getScreen().get_height(), color=(0, 0, 0), alpha=0, visible=False)
        self.__title = self.__scene.getFont(64).render("", True, (255, 255, 255)).convert_alpha()
        self.__subtitle = self.__scene.getFont(32).render("", True, (255, 255, 255)).convert_alpha()
        self.__tick = 0
        self.__wave = 0
        bar_width = scene.getStageManager().getStageConfig().getGridSize() * 2
        bar_height = scene.getStageManager().getStageConfig().getGridSize() * 0.33
        self.__img = pygame.image.load("config/images/UI/diamond_sword.png")
        self.__img = pygame.transform.scale(self.__img, (30, 30))
        self.__waveBg = Button(x=800,y=10,w=bar_width,h=bar_height,color=(0,0,0),text_color=(255,255,255),text_valign="center",text="0",font=scene.getFont(12))
        self.canStart = False

    def trigger(self, wave: int):
        self.__tick = 0
        self.__wave = wave
        self.__background.visible = True
        self.canStart = False

    def drawUI(self):
        self.__waveBg.text = str(self.__wave + 1)
        self.__waveBg.draw(self.__scene.getScreen())

    def tick(self, dt: float, ):
        self.__scene.getScreen().blit(self.__img, (800 - 14, 10 - 6))
        if self.__tick <= 5:
            self.__tick += dt
            if self.__tick < 2.5 and self.__wave > 0:
                self.__title = self.__scene.getFont(64).render(f"Wave {self.__wave} Completed", True,(0, 255, 0)).convert_alpha()
                self.__subtitle = self.__scene.getFont(32).render("Prepare for the next wave", True, (255, 255, 255)).convert_alpha()
            elif self.__tick < 5 and self.__wave > 0:
                self.__title = self.__scene.getFont(64).render("Next Wave", True, (0, 255, 0)).convert_alpha()
                self.__subtitle = self.__scene.getFont(32).render(f"Wave {self.__wave + 1} Incoming", True, (255, 255, 255)).convert_alpha()
            elif self.__tick >= 5:
                self.__background.visible = False
                self.__tick = 100
                self.canStart = True
                self.__scene.getWaveManager().startNextWave()
                return
            alpha255 = min(255, int(255 * min(0.25, self.__tick) / 0.25))
            alpha128 = min(128, int(128 * min(0.25, self.__tick) / 0.25))
            self.__background.alpha = alpha128
            self.__title.set_alpha(alpha255)
            self.__subtitle.set_alpha(alpha255)
            self.__background.draw(self.__scene.getScreen())
            self.__scene.getScreen().blit(self.__title, (self.__width // 2 - self.__title.get_width() // 2, self.__height // 2 - self.__title.get_height() // 2))
            self.__scene.getScreen().blit(self.__subtitle, (self.__width // 2 - self.__subtitle.get_width() // 2, self.__height // 2 + self.__title.get_height() // 2))
