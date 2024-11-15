import pygame
import time

from src.GradientUtils import GradientUtils


class Button:
    def __init__(self, x, y, w, h, rect=None,
                 onHover=None, onHoverStop=None, onLeftClick=None, onRightClick=None,
                 onMiddleClick=None, onLongPress=None, long_press_duration=1.0,
                 visible=True, color=(200, 200, 200, 255), hover_color=(150, 150, 150, 255),
                 selected_color=None,
                 text='', text_color=(0, 0, 0), font=None,
                 text_align='center', text_valign='center', text_offset=(0, 0),
                 image=None,
                 alpha=255, hover_alpha=255, selected_alpha=255,
                 transparent=False,
                 border_width=0, border_color=(0, 0, 0, 255),
                 hover_border_color=None, selected_border_color=None,
                 background_gradient=None,
                 border_gradient=None,
                 text_gradient=None,
                 gradient_utils=None,
                 hover_text=None):
        """
        :param background_gradient: Dict with gradient parameters for the background.
        :param border_gradient: Dict with gradient parameters for the border.
        :param text_gradient: Dict with gradient parameters for the text.
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
        self.onHoverStop = onHoverStop  # New callback for when hover stops
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
        self.transparent = transparent
        self.hovered = False
        self.pressed = False
        self.press_time = None
        self.selected = False
        self.border_width = border_width
        self.border_color = border_color
        self.hover_border_color = hover_border_color if hover_border_color else self.border_color
        self.selected_border_color = selected_border_color if selected_border_color else self.border_color
        self.hover_text = hover_text if hover_text else self.text

        # Gradient parameters
        self.background_gradient = background_gradient  # Dict with gradient params
        self.border_gradient = border_gradient  # Dict with gradient params
        self.text_gradient = text_gradient  # Dict with gradient params

        # GradientUtils instance
        self.gradient_utils = gradient_utils if gradient_utils else GradientUtils()

        # Cached gradient surfaces
        self._background_gradient_surface = None
        self._border_gradient_surface = None
        self._text_gradient_surface = None

    def draw(self, screen):
        if not self.visible:
            return
        if self.transparent and not self.hovered and not self.selected:
            return  # Skip drawing if transparent and neither hovered nor selected

        # Create a surface with per-pixel alpha
        button_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Determine current state and corresponding color and alpha
        text = self.text
        if self.selected:
            color = self.selected_color
            alpha = self.selected_alpha
            border_color = self.selected_border_color
        elif self.hovered:
            color = self.hover_color
            alpha = self.hover_alpha
            border_color = self.hover_border_color
            text = self.hover_text
        else:
            color = self.color
            alpha = self.alpha
            border_color = self.border_color

        # Adjust color with alpha
        color = (*color[:3], alpha)

        # Draw the background
        if self.background_gradient:
            gradient_surface = self._get_background_gradient_surface()
            if gradient_surface:
                button_surface.blit(gradient_surface, (0, 0))
        elif self.image:
            # Draw the image with adjusted alpha
            image = self.image.copy()
            image.set_alpha(alpha)
            button_surface.blit(image, (0, 0))
        else:
            # Draw the rectangle with the current color and alpha
            pygame.draw.rect(button_surface, color, pygame.Rect(0, 0, self.width, self.height))

        # Draw the border if border_width > 0
        if self.border_width > 0:
            if self.border_gradient:
                border_surface = self._get_border_gradient_surface()
                if border_surface:
                    button_surface.blit(border_surface, (0, 0))
            else:
                pygame.draw.rect(button_surface, border_color, pygame.Rect(0, 0, self.width, self.height), width=self.border_width)

        # Draw the text if any
        if text:
            if self.text_gradient:
                text_surf = self._get_text_gradient_surface()
            else:
                text_surf = self.font.render(text, True, self.text_color)
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

    def _get_background_gradient_surface(self):
        if self._background_gradient_surface:
            return self._background_gradient_surface

        grad_params = self.background_gradient
        width, height = self.width, self.height
        colors = grad_params.get('colors')
        gradient_type = grad_params.get('type', 'vertical')

        if not colors:
            return None

        if gradient_type == 'vertical':
            self._background_gradient_surface = self.gradient_utils.get_vertical_gradient(width, height, colors)
        elif gradient_type == 'horizontal':
            self._background_gradient_surface = self.gradient_utils.get_horizontal_gradient(width, height, colors)
        elif gradient_type == 'diagonal':
            self._background_gradient_surface = self.gradient_utils.get_diagonal_gradient(width, height, colors)
        elif gradient_type == 'radial':
            center = grad_params.get('center', None)
            self._background_gradient_surface = self.gradient_utils.get_radial_gradient(width, height, colors, center)
        else:
            return None

        return self._background_gradient_surface

    def _get_border_gradient_surface(self):
        if self._border_gradient_surface:
            return self._border_gradient_surface

        grad_params = self.border_gradient
        width, height = self.width, self.height
        colors = grad_params.get('colors')
        gradient_type = grad_params.get('type', 'vertical')
        border_width = self.border_width

        if not colors or border_width <= 0:
            return None

        border_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        inner_rect = pygame.Rect(border_width, border_width, width - 2 * border_width, height - 2 * border_width)
        mask_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(mask_surface, (0, 0, 0, 0), inner_rect)
        pygame.draw.rect(mask_surface, (255, 255, 255, 255), pygame.Rect(0, 0, width, height), width=border_width)

        if gradient_type == 'vertical':
            gradient = self.gradient_utils.get_vertical_gradient(width, height, colors)
        elif gradient_type == 'horizontal':
            gradient = self.gradient_utils.get_horizontal_gradient(width, height, colors)
        elif gradient_type == 'diagonal':
            gradient = self.gradient_utils.get_diagonal_gradient(width, height, colors)
        elif gradient_type == 'radial':
            center = grad_params.get('center', None)
            gradient = self.gradient_utils.get_radial_gradient(width, height, colors, center)
        else:
            return None

        if gradient:
            border_surface.blit(gradient, (0, 0))
            border_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            self._border_gradient_surface = border_surface
            return self._border_gradient_surface

        return None

    def _get_text_gradient_surface(self):
        if self._text_gradient_surface:
            return self._text_gradient_surface

        grad_params = self.text_gradient
        colors = grad_params.get('colors')
        gradient_type = grad_params.get('type', 'vertical')

        if not colors:
            return None

        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_width, text_height = text_surf.get_size()
        gradient_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)

        if gradient_type == 'vertical':
            gradient = self.gradient_utils.get_vertical_gradient(text_width, text_height, colors)
        elif gradient_type == 'horizontal':
            gradient = self.gradient_utils.get_horizontal_gradient(text_width, text_height, colors)
        elif gradient_type == 'diagonal':
            gradient = self.gradient_utils.get_diagonal_gradient(text_width, text_height, colors)
        elif gradient_type == 'radial':
            center = grad_params.get('center', None)
            gradient = self.gradient_utils.get_radial_gradient(text_width, text_height, colors, center)
        else:
            return None

        if gradient:
            text_mask = text_surf.copy()
            text_mask.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            gradient_surface.blit(gradient, (0, 0))
            gradient_surface.blit(text_mask, (0, 0), None, pygame.BLEND_RGBA_MULT)
            self._text_gradient_surface = gradient_surface
            return self._text_gradient_surface

        return text_surf

    def handle_event(self, event):
        if not self.visible or self.alpha == 0:
            return
        mouse_pos = pygame.mouse.get_pos()
        was_hovered = self.hovered  # Store previous hover state
        if self.rect.collidepoint(mouse_pos):
            if self.onHover:
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
            if was_hovered and self.onHoverStop:
                self.onHoverStop()  # Call onHoverStop when hover ends
            self.hovered = False
            self.pressed = False
            self.press_time = None