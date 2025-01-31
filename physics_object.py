import pygame
import utilities


class PhysicsObject:
    def __init__(self, x, y, mass, radius):
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.mass = mass
        self.radius = radius
        self.forces = pygame.math.Vector2(0, 0)

    def apply_force(self, force):
        self.forces += force

    def update(self, dt):
        acceleration = self.forces / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.forces = pygame.math.Vector2(0, 0)

    def apply_gravity(self, planets):
        for planet in planets:
            utilities.calculate_gravitational_force(self, planet, G=200)

    def draw(self, screen, camera):
        draw_pos = camera.apply(self)
        radius = camera.get_zoomed_value(self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(draw_pos.x), int(draw_pos.y)), radius)