import pygame
import sys

pygame.init()

RED = (255, 0, 0)
LIGHT_RED = (255, 100, 100)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (200,200,200)
DARK_GREY = (100,100,100)

TEXT_FONT_SMALL = pygame.font.SysFont('Arial', 16)
TEXT_FONT_MIDDLE = pygame.font.SysFont('Arial', 50)
TEXT_FONT_LARGE = pygame.font.SysFont('Arial', 75)

main_menu_background = pygame.image.load("D:/pygame project/PygameProject/PygameProject/config/images/Home/foreground.png")
start_image = pygame.image.load("D:/pygame project/PygameProject/PygameProject/config/images/Home/start.png")