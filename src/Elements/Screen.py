import logging
import sys
import pygame
from random import random
from math import sqrt, pi
from typing import TYPE_CHECKING

from src import Events

from game_data import Tower, Bullet, Enemy, box_genreator_from_center
from dataclasses import dataclass,field
from pygame.locals import *

RED = (255, 0, 0)
LIGHT_RED = (255, 100, 100)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

if TYPE_CHECKING:
    from Game import Main

def distance(x : float, y : float) -> float:
    return sqrt(x*x+y*y)

def degree_to_radian(degree: float) -> float:
    return degree/(2*pi)

TEXT_FONT = pygame.font.SysFont('Arial', 16)

class Screen:
    def __init__(self, main: 'Main'):
        self.__main = main
        self.__screen = None
        
        try:
            screen_width = main.getConfig().getScreenWidth()
            screen_height = main.getConfig().getScreenHeight()
            self.__screen = pygame.display.set_mode(
                (screen_width, screen_height)
            )

            pygame.display.set_caption("Pygame Project")
            logging.info(f"Pygame initialized with screen size ({screen_width}x{screen_height}).")
        except pygame.error as e:
            logging.error(f"Error initializing Pygame self.__screen: {e}")
            sys.exit(1)
        
        @dataclass
        class Button:
            rect: pygame.Rect = field(default_factory=pygame.Rect)
            colour: tuple[int] = WHITE
            colour_pressed: tuple[int] = LIGHT_RED
            pressed: bool = False

            def draw(self) -> None:
                pygame.draw.rect(pygame.display.get_surface(), self.colour, self.rect)
                
            def press(self) -> None:
                self.pressed = not self.pressed
                self.colour, self.colour_pressed = self.colour_pressed, self.colour
        
        
        @dataclass
        class CheckBox:
            rect: pygame.Rect = field(default_factory=pygame.Rect)
            isChecked: bool = False
            colour: tuple[int] = RED
            
            def draw(self) -> None:
                pygame.draw.rect(pygame.display.get_surface(), self.colour, self.rect)
            
            def checked(self) -> None:
                if self.isChecked:
                    self.colour = RED
                    self.isChecked = False
                else:
                    self.colour = GREEN
                    self.isChecked = True

            
        self.isPlacing: CheckBox = CheckBox(rect=pygame.Rect(100,500,25,25))
        self.isDeleting: CheckBox = CheckBox(rect=pygame.Rect(100,550,25,25))
        self.checkboxes: list[CheckBox] = [self.isPlacing,self.isDeleting]
    
        self.shoot_button: Button = Button(rect=pygame.Rect(200,500,50,25), colour=WHITE)
        self.buttons: list[Button] = [self.shoot_button]
        
        self.background_grids: list[pygame.Rect] = []
        
    def isNormalState(self) -> bool:
        return not self.isPlacing.isChecked and not self.isDeleting.isChecked
    
    def draw_text(self, text: str, font: pygame.font, colour: tuple[float], coordinate: tuple[float]) -> None:
        img = font.render(text, True, colour)
        self.__screen.blit(img, coordinate)
        
    def screen1(self):
        mouse_coor = self.__main.mouse_coor
        SCREEN_WIDTH = self.__main.getConfig().getScreenWidth()
        SCREEN_HEIGHT = self.__main.getConfig().getScreenHeight()
    #----------BACKGROUND----------#
         
        
        # Draw the path and background
        
        try:
            self.__main.getStageManager().getBackground().draw()
            self.__main.getStageManager().getPath().draw()
        except Exception as e:
            logging.error(f"Error drawing StageManager: {e}")
        
    #-----------LAYER1-------------#
        # Draw enemies
        try:
            self.__main.getWaveManager().draw(self.__screen)
        except Exception as e:
            logging.error(f"Error drawing enemies: {e}")

        self.__main.getUIManager().updateHealthBar()
        self.background_grids: list[pygame.Rect] = [pygame.Rect(box_genreator_from_center(((32+960/15*(i)),(95+640/10*(j))),64,64)) for i in range(15) for j in range(10)]  
        #Tower placing
        if self.__main.mouse_rect.collidelist(self.background_grids) != -1 and self.isNormalState():
            for tower in self.__main.mouse_rect.collideobjectsall(self.__main.towers_placed, key=lambda o: o.hitbox):
                pygame.draw.circle(self.__screen, LIGHT_BLUE, tower.position, tower.range_radius)
        for tower in self.__main.towers_placed:
            if tower not in self.__main.mouse_rect.collideobjectsall(self.__main.towers_placed, key=lambda o: o.hitbox) or not self.isDeleting.isChecked:
                pygame.draw.rect(self.__screen, BLUE, tower.hitbox)
            else:
                pygame.draw.rect(self.__screen, LIGHT_BLUE, tower.hitbox)
    #-----------LAYER2-------------#
        if self.isNormalState():
            if len(self.__main.mouse_rect.collideobjectsall(self.__main.towers_placed, key=lambda o: o.hitbox)) > 0:
                for tower in self.__main.mouse_rect.collideobjectsall(self.__main.towers_placed, key=lambda o: o.hitbox):
                    _ = 0;
                    pygame.draw.rect(self.__screen, WHITE, (mouse_coor[0], mouse_coor[1], 120, 50))
                    for text in tower.info:
                        self.draw_text(text, TEXT_FONT, BLACK, (mouse_coor[0],mouse_coor[1] + _))
                        _ += 16
           #pygame.font.Font.render(tower.info_str)
    #-----------LAYER3-------------#
        #Bullet
        for bullet in self.__main.bullets:
            if bullet.position[0] >= SCREEN_WIDTH + 1000 or bullet.position[0] <= 0 - 1000 or bullet.position[1] >= SCREEN_HEIGHT + 1000 or bullet.position[1] <= 0 - 1000:
                self.__main.bullets.remove(bullet)
                del bullet
                continue
            pygame.draw.circle(self.__screen, GREEN, bullet.position, 10)
        
        
    #----------FOREGROUND----------#
        self.isPlacing.draw(); self.draw_text("Placing",  TEXT_FONT, WHITE, (130,500))
        self.isDeleting.draw(); self.draw_text("Deleting",  TEXT_FONT, WHITE, (130,550))
        self.shoot_button.draw(); self.draw_text("Shooting", TEXT_FONT, WHITE, (275,500))
        if self.isPlacing.isChecked:
            self.__main.tower_at_mouse = pygame.draw.rect(self.__screen, GREEN, box_genreator_from_center(mouse_coor,50,50))
            
        #for grid in self.background_grids:
        #    pygame.draw.rect(self.__screen, WHITE, grid)
    
    ...
    
    def screen2(self):
        #----------BACKGROUND----------#
        #-----------LAYER1-------------#
        ...
    ... 
        
     
    def screen3(self):
        #----------BACKGROUND----------#
        #-----------LAYER1-------------#
        ...
    ...
    
    

    def draw(self, deltaTime: float):
        # Update wave manager and enemies
        try:
            self.__main.getWaveManager().update(deltaTime)
        except Exception as e:
            logging.error(f"Error updating WaveManager: {e}")
        
        def is_mouse_hitting_towers() -> bool:
            return len(self.__main.mouse_rect.collideobjectsall(self.__main.towers_placed, key=lambda o: o.hitbox)) > 0
        
        def is_mouse_hitting_grids() -> bool:
            return self.__main.mouse_rect.collidelist(self.background_grids) != -1
        
        def is_mouse_hitting_checkboxes() -> bool:
            return len(self.__main.mouse_rect.collideobjectsall(self.checkboxes, key=lambda o: o.rect)) > 0
        
        def is_mouse_hitting_buttons() -> bool:
            return len(self.__main.mouse_rect.collideobjectsall(self.buttons, key=lambda o: o.rect)) > 0
        
        match self.__main.screen_num:
            case 1:
                self.screen1()
            case 2:
                self.screen2()
            case 3:
                self.screen3()
            case _:
                ...       
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == Events.PLAYER_GAME_OVER:
                self.__main.running = False
            elif event.type == Events.ENEMY_REACHED_END:
                self.__main.getPlayer().doDamage(event.enemy)
                #TODO: VICTORY EVENT
            if event.type == MOUSEBUTTONDOWN:
                if is_mouse_hitting_checkboxes():
                    for checkbox in self.__main.mouse_rect.collideobjectsall(self.checkboxes, key=lambda o: o.rect):
                        checkbox.checked()
                    logging.info(f"Checkbox checked.")
                elif is_mouse_hitting_buttons():
                    for button in self.__main.mouse_rect.collideobjectsall(self.buttons, key=lambda o: o.rect):
                        button.press()
                    logging.info(f"Button clicked.")
                    if self.shoot_button.pressed:
                        for tower in self.__main.towers_placed:
                            self.__main.bullets.append(tower.generate_bullet(box_genreator_from_center(tower.position,10,10)))
                else:
                    if self.isPlacing.isChecked:
                        if is_mouse_hitting_grids():
                            grid = self.background_grids[self.__main.mouse_rect.collidelist(self.background_grids)]
                            logging.info(f"Tower placed.")
                            self.__main.towers_placed.append(Tower(position=(grid[0]+grid[2]/2,grid[1]+grid[3]/2), hitbox=grid,angle_rotation=random()*2*pi))
                    elif self.isDeleting.isChecked:
                        if is_mouse_hitting_towers():
                            for tower in self.__main.mouse_rect.collideobjectsall(self.__main.towers_placed, key=lambda o: o.hitbox):
                                self.__main.towers_placed.remove(tower)
                                del tower
            if event.type == MOUSEBUTTONUP:
                for button in self.__main.mouse_rect.collideobjectsall(self.buttons, key=lambda o: o.rect):
                    if button.pressed:
                        button.press()
             
       
        # Update the self.__screen
        try:
            pygame.display.flip()
        except Exception as e:
            logging.error(f"Error updating self.__screen: {e}")

    def getScreen(self):
        return self.__screen

if __name__ == "__main__":
    Screen().__main.run()