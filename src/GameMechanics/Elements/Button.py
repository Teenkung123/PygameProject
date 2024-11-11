import pygame
import time

class Button:
    def __init__(self, x, y, w, h, rect=None,
                 onHover=None, onLeftClick=None, onRightClick=None,
                 onMiddleClick=None, onLongPress=None, long_press_duration=1.0,
                 visible=True, color=(200, 200, 200, 255), hover_color=(150, 150, 150, 255),
                 selected_color=None,
                 text='', text_color=(0, 0, 0), font=None,
                 text_align='center', text_valign='center', text_offset=(0, 0),
                 image=None,
                 alpha=255, hover_alpha=255, selected_alpha=255,
                 transparent=False):
        """
        :param text_align: Horizontal alignment of the text ('left', 'center', 'right')
        :param text_valign: Vertical alignment of the text ('top', 'center', 'bottom')
        :param text_offset: A tuple (x_offset, y_offset) to adjust text position
        """
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        if rect is None:
            self.rect = pygame.Rect(x, y, w, h)
        else:
            self.rect = rect
        self.onHover = onHover
        self.onLeftClick = onLeftClick
        self.onRightClick = onRightClick
        self.onMiddleClick = onMiddleClick
        self.onLongPress = onLongPress
        self.long_press_duration = long_press_duration
        self.visible = visible
        self.color = color  # RGBA color
        self.hover_color = hover_color  # RGBA color
        self.selected_color = selected_color if selected_color else self.color
        self.text = text
        self.text_color = text_color
        self.font = font if font is not None else pygame.font.Font(None, 36)
        self.text_align = text_align
        self.text_valign = text_valign
        self.text_offset = text_offset
        self.image = image
        self.alpha = alpha
        self.hover_alpha = hover_alpha
        self.selected_alpha = selected_alpha
        self.transparent = transparent  # Determines if the button is fully transparent when idle
        self.hovered = False
        self.pressed = False
        self.press_time = None
        self.selected = False  # Tracks whether the button is selected

    def draw(self, screen):
        if not self.visible:
            return
        if self.transparent and not self.hovered and not self.selected:
            return  # Skip drawing if transparent and neither hovered nor selected

        # Create a surface with per-pixel alpha
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Determine current state and corresponding color and alpha
        if self.selected:
            color = self.selected_color
            alpha = self.selected_alpha
        elif self.hovered:
            color = self.hover_color
            alpha = self.hover_alpha
        else:
            color = self.color
            alpha = self.alpha

        # Adjust color with alpha
        color = (*color[:3], alpha)

        if self.image:
            # Draw the image with adjusted alpha
            image = self.image.copy()
            image.set_alpha(alpha)
            button_surface.blit(image, (0, 0))
        else:
            # Draw the rectangle with the current color and alpha
            pygame.draw.rect(button_surface, color, pygame.Rect(0, 0, self.width, self.height))

        # Draw the text if any
        if self.text:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect()

            # Horizontal alignment
            if self.text_align == 'left':
                text_rect.left = self.text_offset[0]
            elif self.text_align == 'center':
                text_rect.centerx = self.width // 2 + self.text_offset[0]
            elif self.text_align == 'right':
                text_rect.right = self.width + self.text_offset[0]

            # Vertical alignment
            if self.text_valign == 'top':
                text_rect.top = self.text_offset[1]
            elif self.text_valign == 'center':
                text_rect.centery = self.height // 2 + self.text_offset[1]
            elif self.text_valign == 'bottom':
                text_rect.bottom = self.height + self.text_offset[1]

            button_surface.blit(text_surf, text_rect)

        # Blit the button surface onto the main screen
        screen.blit(button_surface, (self.x, self.y))

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered and self.onHover:
                self.onHover()
            self.hovered = True

            # Handle Mouse Button Down Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.pressed = True
                    self.press_time = time.time()
                elif event.button == 2 and self.onMiddleClick:  # Middle click
                    self.onMiddleClick()
                elif event.button == 3 and self.onRightClick:  # Right click
                    self.onRightClick()

            # Handle Mouse Button Up Events
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click released
                    if self.pressed:
                        press_duration = time.time() - self.press_time
                        if press_duration >= self.long_press_duration and self.onLongPress:
                            self.onLongPress()
                        elif self.onLeftClick:
                            self.onLeftClick()
                    self.pressed = False
                    self.press_time = None
        else:
            self.hovered = False
            self.pressed = False
            self.press_time = None
