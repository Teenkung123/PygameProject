from typing import TYPE_CHECKING

from src.Utils.Button import Button

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene
    from src.GameMechanics.Entities.Enemy import Enemy


# noinspection PyMethodMayBeStatic
class DebuffIndicator:
    def __init__(self, scene: 'GameScene'):
        self.__scene = scene
        self.__overlays = {}  # Map of enemy IDs to their overlay Buttons

    def tick(self, dt: float):
        enemies = self.__scene.getWaveManager().getEnemies()

        # Keep track of current enemy IDs
        current_enemy_ids = set()

        for enemy in enemies:
            enemy: 'Enemy' = enemy
            enemy_id = id(enemy)  # Use the built-in id() function for uniqueness
            current_enemy_ids.add(enemy_id)

            # Check if enemy has any debuffs
            debuffs = enemy.getDebuffs()
            if debuffs:
                # If overlay doesn't exist, create one
                if enemy_id not in self.__overlays:
                    overlay = self.__create_overlay(enemy)
                    self.__overlays[enemy_id] = overlay
                else:
                    overlay = self.__overlays[enemy_id]
                    self.__update_overlay_position(overlay, enemy)
                # Update overlay color based on current debuffs
                overlay_color = self.__get_overlay_color(debuffs)
                overlay.color = overlay_color[:3]  # RGB color
                overlay.alpha = overlay_color[3]   # Alpha value
            else:
                # Remove overlay if enemy has no debuffs
                if enemy_id in self.__overlays:
                    del self.__overlays[enemy_id]

        # Remove overlays for enemies that no longer exist
        overlay_enemy_ids = set(self.__overlays.keys())
        enemies_to_remove = overlay_enemy_ids - current_enemy_ids
        for enemy_id in enemies_to_remove:
            del self.__overlays[enemy_id]

    def draw(self):
        screen = self.__scene.getScreen()  # Assuming GameScene has a getScreen() method
        for overlay in self.__overlays.values():
            overlay.draw(screen)

    def __create_overlay(self, enemy: 'Enemy') -> 'Button':
        # Create an overlay Button to indicate debuff
        enemy_rect = enemy.getRect()
        overlay_width = enemy_rect.width
        overlay_height = enemy_rect.height  # Make the overlay the same height as the enemy

        # Position the overlay at the same position as the enemy
        overlay_x = enemy_rect.x
        overlay_y = enemy_rect.y

        # Determine color based on debuff types (customize as needed)
        debuffs = enemy.getDebuffs()
        overlay_color = self.__get_overlay_color(debuffs)

        overlay = Button(
            x=overlay_x,
            y=overlay_y,
            w=overlay_width,
            h=overlay_height,
            visible=True,
            color=overlay_color[:3],  # RGB color
            alpha=overlay_color[3],   # Alpha value
            border_width=0,
            text='',  # No text
            transparent=False
        )

        return overlay

    def __update_overlay_position(self, overlay: 'Button', enemy: 'Enemy'):
        # Update overlay position to match the enemy
        enemy_rect = enemy.getRect()
        overlay_width = enemy_rect.width
        overlay_height = enemy_rect.height  # Match the enemy's height

        overlay.x = enemy_rect.x
        overlay.y = enemy_rect.y
        overlay.width = overlay_width
        overlay.height = overlay_height
        overlay.rect.topleft = (overlay.x, overlay.y)

    def __get_overlay_color(self, debuffs) -> tuple:
        # Customize overlay color based on debuff types
        # Example: Different colors for different debuff types
        if any(debuff['type'] == 'burning' for debuff in debuffs):
            return 255, 69, 0, 128  # Orange with alpha for burning
        elif any(debuff['type'] == 'bleeding' for debuff in debuffs):
            return 220, 20, 60, 128  # Crimson with alpha for bleeding
        elif any(debuff['type'] == 'speed_reduction' for debuff in debuffs):
            return 30, 144, 255, 128  # Dodger blue with alpha for slow
        else:
            return 255, 0, 0, 128  # Default red color with alpha
