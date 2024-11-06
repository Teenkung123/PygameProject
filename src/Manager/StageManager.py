import logging

import pygame

from src.Elements.BackgroundElement import BackgroundElement
from src.Elements.PathElement import PathElement
from src.Manager.StageConfig import StageConfig


class StageManager:
    
    def __init__(self, main, stage: str):
        """
        Initialize the StageManager.

        :param main: Instance of Main class
        :param stage: Name of the stage (e.g., "default")
        """
        self.__main = main
        logging.info(f"StageManager Initialized with Project Root: {main.getProjectRoot()}")

        # Load stage-specific config
        self.__stageConfig = StageConfig(main.getProjectRoot(), stage)
        
        self.__background = BackgroundElement(self.__stageConfig, main.getConfig(),  main.getScreen())
        self.__path = PathElement(self.__stageConfig, main, main.getScreen())

    def getStageConfig(self):
        """
        Return the StageConfig instance.
        """
        return self.__stageConfig
    
    def getBackground(self):
        """
        Return the BackgroundElement instance.
        """
        return self.__background
    
    def getPath(self):
        """
        Return the PathElement instance.
        """
        return self.__path
