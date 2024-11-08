import pygame
from typing import List, Tuple, Optional

class GradientUtils:
    def __init__(self):
        """
        Initializes the GradientUtils class with an empty cache.
        """
        self.cache = {}

    def get_vertical_gradient(
        self, width: int, height: int, colors: List[Tuple[int, int, int]]
    ) -> Optional[pygame.Surface]:
        """
        Creates or retrieves a vertical gradient surface with multi-color support.

        :param width: Width of the gradient surface.
        :param height: Height of the gradient surface.
        :param colors: List of RGB tuples representing colors from top to bottom.
        :return: Pygame Surface with the vertical gradient or None if an error occurs.
        """
        key = ('vertical', width, height, tuple(colors))
        if key in self.cache:
            return self.cache[key]

        try:
            gradient = pygame.Surface((width, height))
            num_colors = len(colors)
            if num_colors < 2:
                raise ValueError("At least two colors are required for a gradient.")

            segment_height = height / (num_colors - 1)
            for i in range(num_colors - 1):
                start_color = colors[i]
                end_color = colors[i + 1]
                for y in range(int(segment_height)):
                    factor = y / segment_height
                    color = self._interpolate_color(start_color, end_color, factor)
                    pos_y = int(i * segment_height + y)
                    if pos_y >= height:
                        break
                    pygame.draw.line(gradient, color, (0, pos_y), (width, pos_y))
            self.cache[key] = gradient
            return gradient
        except Exception as e:
            print(f"Error creating vertical gradient: {e}")
            return None

    def get_horizontal_gradient(
        self, width: int, height: int, colors: List[Tuple[int, int, int]]
    ) -> Optional[pygame.Surface]:
        """
        Creates or retrieves a horizontal gradient surface with multi-color support.

        :param width: Width of the gradient surface.
        :param height: Height of the gradient surface.
        :param colors: List of RGB tuples representing colors from left to right.
        :return: Pygame Surface with the horizontal gradient or None if an error occurs.
        """
        key = ('horizontal', width, height, tuple(colors))
        if key in self.cache:
            return self.cache[key]

        try:
            gradient = pygame.Surface((width, height))
            num_colors = len(colors)
            if num_colors < 2:
                raise ValueError("At least two colors are required for a gradient.")

            segment_width = width / (num_colors - 1)
            for i in range(num_colors - 1):
                start_color = colors[i]
                end_color = colors[i + 1]
                for x in range(int(segment_width)):
                    factor = x / segment_width
                    color = self._interpolate_color(start_color, end_color, factor)
                    pos_x = int(i * segment_width + x)
                    if pos_x >= width:
                        break
                    pygame.draw.line(gradient, color, (pos_x, 0), (pos_x, height))
            self.cache[key] = gradient
            return gradient
        except Exception as e:
            print(f"Error creating horizontal gradient: {e}")
            return None

    def get_diagonal_gradient(
        self, width: int, height: int, colors: List[Tuple[int, int, int]]
    ) -> Optional[pygame.Surface]:
        """
        Creates or retrieves a diagonal gradient surface with multi-color support.

        :param width: Width of the gradient surface.
        :param height: Height of the gradient surface.
        :param colors: List of RGB tuples representing colors along the diagonal.
        :return: Pygame Surface with the diagonal gradient or None if an error occurs.
        """
        key = ('diagonal', width, height, tuple(colors))
        if key in self.cache:
            return self.cache[key]

        try:
            gradient = pygame.Surface((width, height))
            num_colors = len(colors)
            if num_colors < 2:
                raise ValueError("At least two colors are required for a gradient.")

            max_distance = (width**2 + height**2) ** 0.5
            for y in range(height):
                for x in range(width):
                    distance = (x + y) / (width + height)
                    color = self._get_multi_color(colors, distance)
                    gradient.set_at((x, y), color)
            self.cache[key] = gradient
            return gradient
        except Exception as e:
            print(f"Error creating diagonal gradient: {e}")
            return None

    def get_radial_gradient(
        self, width: int, height: int, colors: List[Tuple[int, int, int]], center: Optional[Tuple[int, int]] = None
    ) -> Optional[pygame.Surface]:
        """
        Creates or retrieves a radial gradient surface with multi-color support.

        :param width: Width of the gradient surface.
        :param height: Height of the gradient surface.
        :param colors: List of RGB tuples representing colors from center to edge.
        :param center: Tuple representing the center point (x, y). Defaults to center of surface.
        :return: Pygame Surface with the radial gradient or None if an error occurs.
        """
        key = ('radial', width, height, tuple(colors), center)
        if key in self.cache:
            return self.cache[key]

        try:
            gradient = pygame.Surface((width, height), pygame.SRCALPHA)
            if center is None:
                center = (width // 2, height // 2)
            max_distance = ((max(center[0], width - center[0])) ** 2 + (max(center[1], height - center[1])) ** 2) ** 0.5
            num_colors = len(colors)
            if num_colors < 2:
                raise ValueError("At least two colors are required for a gradient.")

            for y in range(height):
                for x in range(width):
                    dx = x - center[0]
                    dy = y - center[1]
                    distance = (dx**2 + dy**2) ** 0.5 / max_distance
                    if distance > 1:
                        distance = 1
                    color = self._get_multi_color(colors, distance)
                    gradient.set_at((x, y), (*color, 255))
            self.cache[key] = gradient
            return gradient
        except Exception as e:
            print(f"Error creating radial gradient: {e}")
            return None

    def clear_cache(self):
        """
        Clears the gradient cache.
        """
        self.cache.clear()

    def _interpolate_color(
        self, start_color: Tuple[int, int, int], end_color: Tuple[int, int, int], factor: float
    ) -> Tuple[int, int, int]:
        """
        Interpolates between two colors by a factor.

        :param start_color: RGB tuple for the start color.
        :param end_color: RGB tuple for the end color.
        :param factor: Float between 0 and 1 representing the interpolation factor.
        :return: Interpolated RGB color.
        """
        return (
            int(start_color[0] + (end_color[0] - start_color[0]) * factor),
            int(start_color[1] + (end_color[1] - start_color[1]) * factor),
            int(start_color[2] + (end_color[2] - start_color[2]) * factor),
        )

    def _get_multi_color(self, colors: List[Tuple[int, int, int]], position: float) -> Tuple[int, int, int]:
        """
        Gets the interpolated color for a position in a multi-color gradient.

        :param colors: List of RGB color tuples.
        :param position: Float between 0 and 1 indicating the position in the gradient.
        :return: Interpolated RGB color.
        """
        num_colors = len(colors)
        total_segments = num_colors - 1
        segment = int(position * total_segments)
        if segment >= total_segments:
            segment = total_segments - 1
            factor = 1.0
        else:
            segment_start = segment / total_segments
            segment_end = (segment + 1) / total_segments
            factor = (position - segment_start) / (segment_end - segment_start)

        start_color = colors[segment]
        end_color = colors[segment + 1]
        return self._interpolate_color(start_color, end_color, factor)
