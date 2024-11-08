import logging

import pygame
import sys
import os

from ConfigLoader import ConfigLoader
from src.EventHandler import EventHandler
from src.GradientUtils import GradientUtils
from src.Scenes.GameScene import GameScene
from src.Scenes.MainMenuScene import MainMenuScene


class Main:
    def __init__(self):
        self.__running = True
        pygame.init()
        self.__projectRoot = os.path.dirname(os.path.abspath(__file__))
        self.__config = ConfigLoader(os.path.join(self.__projectRoot, "config", "config.json"))
        self.__eventHandler = EventHandler(self)
        self.__screen = None
        self.__gradientUtils = GradientUtils()
        self.__initScreen__()
        self.__fontCache = {}

        self.__scenes = {
            "game": GameScene(self),
            "main": MainMenuScene(self)
        }

        self.__currentScene = self.__scenes["main"]

    def __initScreen__(self):
        try:
            screen_width = self.__config.getScreenWidth()
            screen_height = self.__config.getScreenHeight()
            self.__screen = pygame.display.set_mode((screen_width, screen_height))

            pygame.display.set_caption("Pygame Project")
            logging.info(f"Pygame initialized with screen size ({screen_width}x{screen_height}).")
        except pygame.error as e:
            logging.error(f"Error initializing Pygame display: {e}")
            sys.exit(1)

    def run(self):
        clock = pygame.time.Clock()
        while self.__running:
            self.__eventHandler.handle()
            self.__currentScene.tick(clock.tick(60) / 1000.0)

            # Update the display
            try:
                pygame.display.flip()
            except Exception as e:
                logging.error(f"Error updating display: {e}")

        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    def getConfig(self) -> ConfigLoader:
        return self.__config

    def getFont(self, size: int) -> pygame.font.Font:
        if size not in self.__fontCache:
            self.__fontCache[size] = pygame.font.Font('Kanit-Regular.ttf', size)
        return self.__fontCache[size]

    def getGradientUtils(self) -> GradientUtils:
        return self.__gradientUtils

    def getProjectRoot(self) -> str:
        return self.__projectRoot

    def setRunning(self, running: bool):
        self.__running = running

    def getCurrentScene(self):
        return self.__currentScene

    def getCurrentSceneName(self):
        for key, value in self.__scenes.items():
            if value == self.__currentScene:
                return key
        return None

    def setCurrentScene(self, sceneName: str):
        if sceneName in self.__scenes:
            self.__currentScene = self.__scenes[sceneName]
        else:
            raise ValueError(f"Scene {sceneName} does not exist.")

    def getScreen(self):
        return self.__screen

    def resetScene(self, sceneName: str):
        self.__scenes[sceneName] = None
        if sceneName == "game":
            self.__scenes[sceneName] = GameScene(self)
        elif sceneName == "main":
            self.__scenes[sceneName] = MainMenuScene(self)
        else:
            raise ValueError(f"Scene {sceneName} does not exist.")