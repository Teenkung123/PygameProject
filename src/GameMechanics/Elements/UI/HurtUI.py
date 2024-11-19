from src.Utils.Button import Button
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class HurtUI:
    def __init__(self, gameScene: 'GameScene'):
        self.__gameScene = gameScene
        w = gameScene.getScreen().get_width()
        h = gameScene.getScreen().get_height()
        self.__button = Button(0,0,w, h,color=(255,0,0),alpha=0)
        self.__delay = 0

    def tick(self, dt):
        self.__button.draw(self.__gameScene.getScreen())
        if self.__delay > 0:
            self.__delay -= dt
            self.__button.alpha = max(self.__delay/0.25 * 128, 0)
            if self.__delay <= 0:
                self.__button.alpha = 0

    def hurt(self):
        self.__button.alpha = 128
        self.__delay = 0.25