from typing import TYPE_CHECKING

from src.GameMechanics.Elements.UI.CurrencyUI import CurrencyUI
from src.GameMechanics.Elements.UI.DebuffIndicator import DebuffIndicator
from src.GameMechanics.Elements.UI.EnemyHealthBar import EnemyHealthBar
from src.GameMechanics.Elements.UI.HealthBarUI import HealthBarUI
from src.GameMechanics.Elements.InventoryElement import InventoryUI
from src.GameMechanics.Elements.UI.HurtUI import HurtUI
from src.GameMechanics.Elements.UI.PauseUI import PauseUI
from src.GameMechanics.Elements.UI.PlayerLostUI import PlayerLostUI
from src.GameMechanics.Elements.UI.PlayerVictoryUI import PlayerVictoryUI
from src.GameMechanics.Elements.UI.TowerStatusUI import TowerStatusUI
from src.GameMechanics.Elements.UI.WaveChangeUI import WaveChangeUI

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class UIManager:
    def __init__(self, gameScene: 'GameScene'):
        self.healthUI = HealthBarUI(gameScene)
        self.currencyUI = CurrencyUI(gameScene)
        self.EnemyHealthUI = EnemyHealthBar(gameScene)
        self.hotbarUI = InventoryUI(gameScene)
        self.hurtUI = HurtUI(gameScene)
        self.pauseUI = PauseUI(gameScene)
        self.towerStatusUI = TowerStatusUI(gameScene)
        self.waveChangeUI = WaveChangeUI(gameScene)
        self.playerVictoryUI = PlayerVictoryUI(gameScene)
        self.playerLostUI = PlayerLostUI(gameScene)
        self.debuffIndicator = DebuffIndicator(gameScene)

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


