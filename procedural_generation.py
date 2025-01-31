import random
import pygame
from planet import Planet

def generate_planets(num_planets, world_size, min_distance=700, min_radius=100, max_radius=300):

    planets = []
    max_attempts = 1000  # To prevent infinite loops

    for _ in range(num_planets):
        attempts = 0
        while attempts < max_attempts:
            # Random position in the world bounds
            x = random.randint(min_radius, world_size[0] - min_radius)
            y = random.randint(min_radius, world_size[1] - min_radius)

            # Random size and mass
            #radius = random.randint(min_radius, max_radius)
            #mass = radius * 250  # Mass scales with size
            radius = 200
            mass = 50000

            # Random color (grayscale or slight color variations)
            color = (
                random.randint(100, 255), 
                random.randint(100, 255), 
                random.randint(100, 255)
            )

            # Ensure it doesn’t overlap with existing planets
            too_close = any((pygame.math.Vector2(x, y) - p.position).length() < (p.radius + radius + min_distance) for p in planets)

            if not too_close:
                planets.append(Planet(x, y, mass, radius, color))
                break  # Move to the next planet

            attempts += 1

    return planets
