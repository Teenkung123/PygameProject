import pygame
import sys
from pygame.locals import *

from dataclasses import dataclass,field
import src.Scenes.Constants as c

@dataclass
class Button:
    image : pygame.Surface = field(default_factory=pygame.Surface)
    rect: pygame.Rect = field(default_factory=pygame.Rect)
    colour: tuple[int] = c.WHITE
    colour_pressed: tuple[int] = c.DARK_GREY
    colour_hovered: tuple[int] = c.LIGHT_GREY
    DISPLAY: pygame.Surface = field(default_factory=pygame.Surface)
    clicked: bool = False
    
    def draw(self) -> bool:
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked == True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        #draw button on the screen
        self.DISPLAY.blit(self.image, self.rect)
        
        return action
   
    
@dataclass
class CheckBox:
    rect: pygame.Rect = field(default_factory=pygame.Rect)
    isChecked: bool = False
    colour: tuple[int] = c.RED
    DISPLAY: pygame.Surface = field(default_factory=pygame.Surface)
    
    def draw(self) -> None:
        pygame.draw.rect(self.DISPLAY, self.colour, self.rect)
    
    def checked(self) -> None:
        if self.isChecked:
            self.colour = c.RED
            self.isChecked = False
        else:
            self.colour = c.GREEN
            self.isChecked = True
 
def draw_text(DISPLAY: pygame.Surface, text: str, font: pygame.font, colour: tuple[float], coordinate: tuple[float]) -> None:
    img = font.render(text, True, colour)
    DISPLAY.blit(img, coordinate)
    
def box_genreator_from_center(center_point: tuple, height:int, width: int) -> pygame.Rect:
    x_topleft: float = center_point[0]-0.5*width
    y_topleft: float = center_point[1]-0.5*height
    return pygame.Rect(x_topleft,y_topleft,width,height)