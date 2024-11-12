import logging
import os.path
import pygame
from pygame import Vector2
from typing import TYPE_CHECKING

from src.Events import PLAYER_INVENTORY_SELECTED
from src.GameMechanics.Elements.Button import Button

if TYPE_CHECKING:
    from src.Scenes.GameScene import GameScene

class InventoryUI:
    def __init__(self, gameScene: 'GameScene'):
        self.selected_slot = None
        self.__main = gameScene
        self.__font = gameScene.getFont(12)
        self.__slotDisplays: dict[int, dict] = {
            0: {},
            1: {},
            2: {},
            3: {},
            4: {},
            5: {},
            6: {},
            7: {},
            8: {}
        }

        self.__loadImage()
        self.__setSlotPosition()
        self.__calculateHotbarPos()
        self.__initButtons()

    def __loadImage(self):
        path = os.path.join(self.__main.getProjectRoot(), "config", "images", "hotbar.png")
        image_path = os.path.normpath(path)
        if not os.path.exists(image_path):
            logging.error(f"InventoryUI image not found: {image_path}")
            raise FileNotFoundError(f"InventoryUI image not found: {image_path}")

        original_image = pygame.image.load(image_path)
        original_width, original_height = original_image.get_size()

        self.__new_width = 584
        self.__scaling_factor = self.__new_width / original_width
        self.__new_height = int(original_height * self.__scaling_factor)
        self.__image = pygame.transform.scale(original_image, (self.__new_width, self.__new_height))
        logging.debug(
            f"Hotbar image scaled by factor {self.__scaling_factor} to size ({self.__new_width}, {self.__new_height})")

    def __setSlotPosition(self):
        self.__original_slot_positions = [
            Vector2(13, 12),
            Vector2(93, 13),
            Vector2(174, 13),
            Vector2(254, 13),
            Vector2(334, 13),
            Vector2(414, 13),
            Vector2(494, 13),
            Vector2(574, 13),
            Vector2(654, 13)
        ]
        logging.debug("Original slot positions defined.")

    def __calculateHotbarPos(self):
        screen_width = self.__main.getConfig().getScreenWidth()
        self.x_position = (screen_width - self.__new_width) // 2
        self.y_position = -4  # Adjust as needed
        logging.debug(f"Hotbar position calculated at ({self.x_position}, {self.y_position})")

    def __initButtons(self):
        self.__buttons = []
        scaled_button_size = 64 * self.__scaling_factor
        for idx, pos in enumerate(self.__original_slot_positions):
            scaled_pos = pos * self.__scaling_factor
            absolute_pos = Vector2(self.x_position + scaled_pos.x, self.y_position + scaled_pos.y)

            def on_left_click(slot_index=idx):
                self.__callButtonEvent(slot_index)
                self.selectSlot(slot_index)

            button = Button(
                x=absolute_pos.x,
                y=absolute_pos.y,
                w=scaled_button_size,
                h=scaled_button_size,
                onLeftClick=on_left_click,
                color=(0, 0, 0, 255),
                hover_color=(0, 0, 0, 128),
                selected_color=(0, 0, 0, 128),
                alpha=255,
                hover_alpha=128,
                selected_alpha=128,
                text="",
                text_color=(255, 128, 0),
                text_valign="bottom",
            )
            self.__buttons.append(button)
        logging.info(f"Initialized {len(self.__buttons)} buttons.")
        self.selected_slot = None  # Keep track of the selected slot

    def selectSlot(self, slot_index):
        # Deselect all buttons
        for idx, button in enumerate(self.__buttons):
            button.selected = (idx == slot_index)
        self.selected_slot = slot_index
        logging.info(f"Slot {slot_index + 1} selected")

    # noinspection PyMethodMayBeStatic
    def __callButtonEvent(self, slot_index):
        # Create and post the custom event with slot index data
        event_data = {"slot": slot_index, "tower": self.__slotDisplays[slot_index].get("name")}
        pygame.event.post(pygame.event.Event(PLAYER_INVENTORY_SELECTED, data=event_data))

    def display(self):
        screen = self.__main.getScreen()
        screen.blit(self.__image, (self.x_position, self.y_position))
        for idx, button in enumerate(self.__buttons):
            if self.__slotDisplays[idx].get("image"):
                button.alpha = 255
                button.image = self.__slotDisplays[idx].get("image")
                button.color = (0, 0, 0, 255)
                button.transparent = False
            else:
                button.alpha = 0
                button.color = (0, 0, 0, 128)
                button.transparent = True
            button.draw(screen)

    def handle_event(self, event):
        for button in self.__buttons:
            button.handle_event(event)

    def setSlot(self, slot: int, data: dict):
        self.__slotDisplays[slot] = data





