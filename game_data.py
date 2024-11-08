import pygame as pg
import sys
import math
from pygame.locals import *
from dataclasses import dataclass,field

pg.init()

INT_MAX = sys.maxsize
INT_MIN = -sys.maxsize

@dataclass
class Bullet:
    damage: float = INT_MAX
    velocity: tuple[float] = (0,0)
    position: list[float] = field(default_factory=list) 
    hitbox: pg.Rect = field(default_factory=pg.Rect)
    
    def decrease_damage(self, to_decrease: int) -> None:
        self.damage -= to_decrease
    
@dataclass
class Tower:
    name: str = "Unnamed"
    delay: float = 1
    range_radius: float = 100
    damage: float = 100
    shooting_speed: float = 500
    buying_cost: int = 0
    selling_cost: int = 0
    angle_rotation: float = 0 # In radian
    position: tuple[float] = (0,0)
    timer: float = 0
    hitbox: pg.Rect = field(default_factory=pg.Rect)
    
    
    def generate_bullet(self, hitbox: pg.Rect) -> Bullet:
        return Bullet(damage=self.damage, 
                      velocity=(self.shooting_speed*math.cos(self.angle_rotation), self.shooting_speed*math.sin(self.angle_rotation)),
                      position=self.position,
                      hitbox=hitbox if hitbox != None else pg.Rect(0,0,0,0))
        #Calculate bullet's velocity based on angle of the tower
    
    def isMouseOn(self, mouse_pos: tuple[float]) -> bool:
        return distance(self.position[0]-mouse_pos[0], self.position[1]-mouse_pos[1]) <= 25
    
    @property
    def info(self) -> tuple[str]:
        return (f"Name: {self.name}",f"Delay: {self.delay} seconds",f"Radius: {self.range_radius}")
               
@dataclass(order=True)
class Enemy:
    name: str = "Unnamed" 
    health: float = 100
    damage: float = 10
    reward: int = 0
    speed: float = 10
    position: list[float] = field(default_factory=list)
    hitbox: pg.Rect = field(default_factory=pg.Rect)
        
    def decrease_health(self, bullet: Bullet) -> None:
        _ = self.health
        self.health -= bullet.damage
        bullet.damage -= min(bullet.damage,_)
    
HEALTH_BASE = 100

def box_genreator_from_center(center_point: tuple, height:int, width: int) -> pg.Rect:
    x_topleft: float = center_point[0]-0.5*width
    y_topleft: float = center_point[1]-0.5*height
    return pg.Rect(x_topleft,y_topleft,height,width)

def distance(x : float, y : float) -> float:
    return math.sqrt(x*x+y*y)

def main() -> None:
    T: Tower = Tower("Archery", angle_rotation= 1.0, hitbox=box_genreator_from_center((0,0),10,10))
    print(T, T.generate_bullet(box_genreator_from_center(T.position,10,10)))
    
if __name__ == "__main__":
    main()
