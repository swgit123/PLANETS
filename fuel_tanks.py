import pygame
import random
from utilities import position_on_orbit

class FuelTank:
    def __init__(self, x, y, radius=1, fuel_amount=150):
        self.position = pygame.math.Vector2(x, y)
        self.radius = radius
        self.fuel_amount = fuel_amount  # Amount of fuel provided by the tank

    def draw(self, screen, camera):
        # Draw the fuel tank as a simple circle
        draw_pos = camera.apply(self)
        pygame.draw.circle(screen, (250, 255, 255), (int(draw_pos.x), int(draw_pos.y)), camera.get_zoomed_value(self.radius), 3)

    def refill(self, spaceship):
        spaceship.fuel_amount = min(spaceship.max_fuel, spaceship.fuel_amount + self.fuel_amount)  # Refill spaceship's fuel
