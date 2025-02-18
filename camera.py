import pygame


class Camera:
    def __init__(self, position, width, height):
        self.position = pygame.math.Vector2(position)
        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2(0, 0)
        self.zoom = 1.0
        self.angle = 0
        self.mouse_influence = 0.01  # How much the mouse movement affects the camera

    def adjust_angle(self, delta_angle):
        """Adjust the camera's angle by delta_angle degrees."""
        self.angle += delta_angle
        self.angle %= 360  # Normalize between 0-360

    def update(self, target):
        """
        Update the camera's position to follow the target and slightly shift towards the mouse position.
        """
        follow_speed = 0.2  # Camera follow smoothing
        target_center = target.position - (pygame.math.Vector2(self.width, self.height) / 2) / self.zoom

        # Get mouse position relative to screen center
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen_center_x = self.width / 2
        screen_center_y = self.height / 2

        # Calculate offset based on mouse movement (scaled)
        mouse_offset_x = (mouse_x - screen_center_x) * self.mouse_influence
        mouse_offset_y = (mouse_y - screen_center_y) * self.mouse_influence

        # Apply target tracking and mouse influence
        new_offset = target_center + pygame.math.Vector2(mouse_offset_x, mouse_offset_y)
        self.offset += (new_offset - self.offset) * follow_speed  # Smooth transition

    def apply(self, entity):
        if isinstance(entity, pygame.math.Vector2):  # Handle raw Vector2 points
            position = (entity - self.offset) * self.zoom
        else:
            position = (entity.position - self.offset) * self.zoom  # Handle objects with .position

        return position
        

    def adjust_zoom(self, amount):
        self.zoom += amount
        self.zoom = max(0.1, min(self.zoom, 5))  # Limit zoom level between 0.1x and 5x

    def get_zoomed_value(self, value):
        return int(value * self.zoom)  # Scale value based on zoom level
