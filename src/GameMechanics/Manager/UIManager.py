from typing import TYPE_CHECKING

from src.GameMechanics.Elements.UI.CurrencyUI import CurrencyUI
from src.GameMechanics.Elements.UI.EnemyHealthBar import EnemyHealthBar
from src.GameMechanics.Elements.UI.GameOverUI import GameOverUI
from src.GameMechanics.Elements.UI.HealthBarUI import HealthBarUI
from src.GameMechanics.Elements.InventoryElement import InventoryUI
from src.GameMechanics.Elements.UI.HurtUI import HurtUI
from src.GameMechanics.Elements.UI.PauseUI import PauseUI
from src.GameMechanics.Elements.UI.TowerStatusUI import TowerStatusUI

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class UIManager:
    def __init__(self, gameScene: 'GameScene'):
        self.gameOverUI = GameOverUI(gameScene)
        self.healthUI = HealthBarUI(gameScene)
        self.currencyUI = CurrencyUI(gameScene)
        self.EnemyHealthUI = EnemyHealthBar(gameScene)
        self.hotbarUI = InventoryUI(gameScene)
        self.hurtUI = HurtUI(gameScene)
        self.pauseUI = PauseUI(gameScene)
        self.towerStatusUI = TowerStatusUI(gameScene)

    def displayGameOver(self):
        self.gameOverUI.display()

    def updateHealthBar(self):
        self.healthUI.display()

    def updateEnemyHealthBar(self):
        self.EnemyHealthUI.display()

    def updateHotbarInventory(self):
        self.hotbarUI.display()

    def updateCurrency(self):
        self.currencyUI.display()

    def getHurtUI(self):
        return self.hurtUI



