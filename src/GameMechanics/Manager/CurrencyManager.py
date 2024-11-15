from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene


class CurrencyManager:
    def __init__(self, gameScene: 'GameScene'):
        self.__gameScene = gameScene
        self.__currencies = {
            "gold": 75
        }

    def getCurrency(self, currencyType: str):
        """
        Get the currency value for the given currency type.
        """
        if currencyType in self.__currencies:
            return self.__currencies[currencyType]
        return 0

    def setCurrency(self, currencyType: str, value: int):
        """
        Set the currency value for the given currency type.
        """
        self.__currencies[currencyType] = value

    def deposit(self, currencyType: str, amount: int):
        """
        Deposit the given amount of currency.
        """
        if currencyType in self.__currencies:
            self.__currencies[currencyType] += amount
        else:
            self.__currencies[currencyType] = amount

    def withdraw(self, currencyType: str, amount: int):
        """
        Withdraw the given amount of currency.
        """
        if currencyType in self.__currencies:
            self.__currencies[currencyType] -= amount
        else:
            self.__currencies[currencyType] = -amount
        if self.__currencies[currencyType] < 0:
            self.__currencies[currencyType] = 0