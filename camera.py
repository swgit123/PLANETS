import pygame


class Camera:
    def __init__(self, position, width, height):
        self.position = pygame.math.Vector2(position)
        self.width = width
        self.height = height
        self.offset = pygame.math.Vector2(0, 0)
        self.zoom = 1.0
        self.angle = 0
        self.mouse_influence = 0.01  # Mouse influence in follow mode
        self.free_camera_speed = 1  # Speed of free camera movement
        self.mode = "follow"  # Default mode

    def toggle_mode(self):
        """Toggle between free camera mode and follow mode."""
        if self.mode == "follow":
            self.mode = "free"
        else:
            self.mode = "follow"

    def update(self, target_position):
        """Update the camera based on the current mode."""
        follow_speed = 0.2  # Smoothing factor

        if self.mode == "follow":
            # Follow mode: Camera follows the target with slight mouse offset
            target_center = target_position - (pygame.math.Vector2(self.width, self.height) / 2) / self.zoom

            # Get mouse position relative to screen center
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen_center_x = self.width / 2
            screen_center_y = self.height / 2

            # Calculate offset based on mouse movement
            mouse_offset_x = (mouse_x - screen_center_x) * self.mouse_influence
            mouse_offset_y = (mouse_y - screen_center_y) * self.mouse_influence

            # Apply target tracking and mouse influence
            new_offset = target_center + pygame.math.Vector2(mouse_offset_x, mouse_offset_y)
            self.offset += (new_offset - self.offset) * follow_speed  # Smooth transition

        elif self.mode == "free":
            # Free camera mode: Move in the direction of the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen_center_x = self.width / 2
            screen_center_y = self.height / 2

            move_x = (mouse_x - screen_center_x) * 0.02  # Scale movement
            move_y = (mouse_y - screen_center_y) * 0.02

            self.offset += pygame.math.Vector2(move_x, move_y) * self.free_camera_speed

    def apply(self, entity):
        """Transform world coordinates to screen coordinates."""
        if isinstance(entity, pygame.math.Vector2):  # Handle raw Vector2 points
            position = (entity - self.offset) * self.zoom
        else:
            position = (entity.position - self.offset) * self.zoom  # Handle objects with .position

        return position

    def adjust_zoom(self, amount):
        """Zoom in or out."""
        self.zoom += amount
        self.zoom = max(0.1, min(self.zoom, 5))  # Limit zoom level

    def get_zoomed_value(self, value):
        """Return value adjusted for zoom."""
        return int(value * self.zoom)
