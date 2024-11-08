
import pygame
import sys
import os
from math import sqrt, pi
from ConfigLoader import ConfigLoader
from src.Elements.Screen import Screen
from src.Entities.Player import Player
from src.EventHandler import EventHandler
from src.Manager.EnemyConfig import EnemyConfig
from src.Manager.StageManager import StageManager
from src.Manager.UIManager import UIManager
from src.Manager.WaveManager import WaveManager

from game_data import Tower, Bullet, Enemy, box_genreator_from_center

FPS = 30

def velocity_to_new_position_with_time_diff(time_different :float, initial_position :list[float], velocity: tuple[float]) -> list[float]:
    final_position: list[float] = [initial_position[0]+velocity[0]*time_different,initial_position[1]+velocity[1]*time_different]
    return final_position

class Main:
    def __init__(self):
        self.__running = True
        pygame.init()
        self.__projectRoot = os.path.dirname(os.path.abspath(__file__))
        self.__config = ConfigLoader(os.path.join(self.__projectRoot, "config", "config.json"))
        self.__enemyConfig = EnemyConfig(self)
        self.__screen = Screen(self)
        self.__stageManager = StageManager(self, "default")
        self.__UIManager = UIManager(self)
        self.__player = Player(self)
        self.__eventHandler = EventHandler(self)
        self.__waveManager = WaveManager(self)
        
        self.towers_placed: list[Tower] = []
        self.bullets: list[Bullet] = []
        self.mouse_coor = (0,0)
        self.mouse_rect = pygame.Rect(self.mouse_coor[0], self.mouse_coor[1], 1, 1)
        
        self.screen_num: int = 1
        
        self.near_tower : Tower
        self.tower_at_mouse : Tower
    def run(self):
        clock = pygame.time.Clock()
        
        
        
        while self.__running:
                
            clock.tick(FPS)
            
            self.mouse_coor = pygame.mouse.get_pos()
            self.mouse_rect = pygame.Rect(self.mouse_coor[0], self.mouse_coor[1], 1, 1)
            
            time_difference_ms: int = clock.get_time()
            time_difference: float = time_difference_ms/1000
            
            for bullet in self.bullets:
                bullet.position = velocity_to_new_position_with_time_diff(time_difference, bullet.position, bullet.velocity)
                bullet.hitbox = box_genreator_from_center(bullet.position, 10, 10)
            
            for tower in self.towers_placed:
                tower.timer += time_difference
                if tower.timer >= tower.delay:
                    self.bullets.append(tower.generate_bullet(box_genreator_from_center(tower.position,10,10)))
                    tower.timer -= tower.delay
            
            
            #self.__eventHandler.handle()
            self.__screen.draw(time_difference)
            

        self.__UIManager.displayGameOver()
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    def getConfig(self) -> ConfigLoader:
        return self.__config

    def getScreen(self) -> pygame.Surface:
        return self.__screen.getScreen()

    def getProjectRoot(self) -> str:
        return self.__projectRoot

    def getStageManager(self) -> StageManager:
        return self.__stageManager

    def getWaveManager(self) -> WaveManager:
        return self.__waveManager

    def getEnemyConfig(self) -> EnemyConfig:
        return self.__enemyConfig

    def getPlayer(self) -> Player:
        return self.__player

    def getUIManager(self) -> UIManager:
        return self.__UIManager

    def setRunning(self, running: bool):
        self.__running = running
        

if __name__ == "__main__":
    Main().run()
