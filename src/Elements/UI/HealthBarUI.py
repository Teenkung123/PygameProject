from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Main import Main

class HealthBarUI:
    def __init__(self, main: 'Main', font):
        self.__main = main
        self.__font = font

    def display(self):
        health_text = self.__font.render(f"Health: {self.__main.getPlayer().getHealth()}", True, (255, 255, 255))
        self.__main.getScreen().blit(health_text, (10, 10))