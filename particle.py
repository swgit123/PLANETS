import pygame
import math
import random


class Particle:
    def __init__(self, x, y, angle, speed, lifetime):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        self.lifetime = lifetime
        self.initial_lifetime = lifetime
        self.size = random.uniform(0.3, 0.8)  # Tiny particles
        self.color = (255, 255, 255) 
        self.collided = False  # Track collision status

    def update(self, dt):
        self.position += self.velocity * dt
        self.lifetime -= 1


    def draw(self, surface, camera):
        if self.lifetime > 0 and not self.collided:
            draw_pos = camera.apply(self)
            # Gradually increase particle size as it moves away
            size = camera.get_zoomed_value(self.size * (1 + (1 - self.lifetime / self.initial_lifetime) * 0.8))
            alpha = max(10, int(255 * (self.lifetime / self.initial_lifetime)))  # Fading out

            # Create a fading particle surface
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (self.color[0], self.color[1], self.color[2], alpha), (size, size), size)

            # Blit the particle onto the main surface
            surface.blit(particle_surface, (draw_pos.x - size, draw_pos.y - size))